//! A Sárkány szeme lemezes változatának tesztje a valódi TVC 1.2 ROM-mal és VT-DOS-szal.
//! ktest <snapshot.rtvcsnap> <lemez.dsk> <parancsfájl>
//! parancsok: type <szöveg> | enter | frames <n> | shot <név> | pc | key <kód> | trace <n> | regs
use rtvc_core::machine_type::ExpansionCard;
use rtvc_core::tvc::Tvc;
use std::io::Write;

fn shot(tvc: &Tvc, name: &str) {
    let w = 608usize;
    let h = tvc.framebuffer.len() / w;
    let mut f = std::fs::File::create(format!("{name}.ppm")).unwrap();
    write!(f, "P6\n{w} {h}\n255\n").unwrap();
    for p in &tvc.framebuffer {
        f.write_all(&[(p >> 16) as u8, (p >> 8) as u8, *p as u8]).unwrap();
    }
    println!("shot {name}");
}

fn regs(tvc: &mut Tvc) {
    let s = &tvc.z80.state;
    let (pc, sp) = (s.pc, s.sp);
    let map = tvc.bus.mmu.get_map_val();
    let p3 = tvc.bus.mmu.r8(0x0003);
    let d1705 = tvc.bus.mmu.r8(0x1705);
    println!("PC={pc:04X} SP={sp:04X} map={map:02X} (0003)={p3:02X} (1705)={d1705:02X} labels={:?}", tvc.bus.mmu.map_labels());
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let roms = "/home/claude/rtvc/roms/";
    let mut tvc = Tvc::new(false);
    for n in ["TVC12_D3.64K", "TVC12_D4.64K", "TVC12_D7.64K"] {
        tvc.add_rom(n, &std::fs::read(format!("{roms}{n}")).unwrap());
    }
    tvc.attach_card(0, ExpansionCard::VtDos12, &std::fs::read(format!("{roms}VT-DOS12-DISK.ROM")).unwrap());
    if a[1] != "-" {
        let data = std::fs::read(&a[1]).unwrap();
        let chunks = rtvc_core::snapshot::read_file(&data).unwrap();
        let chunk = chunks.iter().find(|c| c.id == *b"EMUT").expect("EMUT");
        let machine = rtvc_core::machine_type::MachineType::from_snapshot_chunk(chunk.data).unwrap();
        tvc = Tvc::new(machine.is_plus);
        machine.attach_builtin_cards(&mut tvc);
        for (name, use_) in machine.rom_uses() {
            let p = format!("{roms}{name}");
            if let Ok(bytes) = std::fs::read(&p) {
                rtvc_core::machine_type::place_machine_rom(&mut tvc, &name, &bytes, use_);
            } else { println!("nincs ROM: {name}"); }
        }
        tvc.load_snapshot(&data).expect("snapshot");
    } else {
        tvc.reset();
    }
    tvc.load_disk(0, 0, "a.dsk", &std::fs::read(&a[2]).unwrap());
    let script = std::fs::read_to_string(&a[3]).unwrap();
    let mut frame = 0u64;
    let run = |tvc: &mut Tvc, n: u64, frame: &mut u64| {
        for _ in 0..n { tvc.run_for_a_frame(); *frame += 1; }
    };
    for line in script.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') { continue; }
        let (cmd, arg) = line.split_once(' ').unwrap_or((line, ""));
        match cmd {
            "type" => {
                for ch in arg.chars() {
                    let code = tvc.press_char(ch);
                    run(&mut tvc, 3, &mut frame);
                    tvc.key_up(code);
                    run(&mut tvc, 2, &mut frame);
                }
            }
            "enter" => { let c = tvc.press_char('\n'); run(&mut tvc, 3, &mut frame); tvc.key_up(c); run(&mut tvc, 2, &mut frame); }
            "key" => { let c: u32 = arg.parse().unwrap(); tvc.key_down(c); run(&mut tvc, 4, &mut frame); tvc.key_up(c); run(&mut tvc, 2, &mut frame); }
            "kd" => { tvc.key_down(arg.parse().unwrap()); }
            "ku" => { tvc.key_up(arg.parse().unwrap()); }
            "frames" => run(&mut tvc, arg.parse().unwrap(), &mut frame),
            "shot" => shot(&tvc, arg),
            "pc" | "regs" => { print!("f{frame} "); regs(&mut tvc); }
            "trace" => {
                let n: u32 = arg.parse().unwrap();
                for _ in 0..n { let pc = tvc.z80.state.pc; let map = tvc.bus.mmu.get_map_val(); print!("{pc:04X}/{map:02X} "); tvc.debug_step_instruction(); }
                println!();
            }
            "bp" => {
                // bp <n képkocka> <cím,cím,...>: ezeken a címeken kiírja PC/SP-t
                let (n, list) = arg.split_once(' ').unwrap();
                let n: u64 = n.parse().unwrap();
                let addrs: Vec<u16> = list.split(',').map(|x| u16::from_str_radix(x, 16).unwrap()).collect();
                let mut cyc: u64 = 0;
                while cyc < n * 62400 {
                    let pc = tvc.z80.state.pc;
                    if addrs.contains(&pc) && tvc.bus.mmu.map_labels()[(pc >> 14) as usize].starts_with('U') {
                        println!("bp {pc:04X} SP={:04X}", tvc.z80.state.sp);
                    }
                    cyc += tvc.debug_step_instruction() as u64;
                }
                frame += n;
            }
            "fuzz" => {
                // fuzz <képkocka> <mag> <veremalja hex> <verem teteje hex>: véletlen billentyűk, őrző + a lemezverem legmélyebb pontja
                let p: Vec<&str> = arg.split(' ').collect();
                let n: u64 = p[0].parse().unwrap(); let mut seed: u64 = p[1].parse().unwrap();
                let lo = u16::from_str_radix(p[2], 16).unwrap(); let hi = u16::from_str_radix(p[3], 16).unwrap();
                let keys = [32u32, 32, 32, 32, 32, 32, 39, 39, 37, 40, 38];
                let mut minsp = 0xFFFFu16; let mut cyc: u64 = 0; let mut next_key = 0u64; let mut down: Option<(u32, u64)> = None;
                let mut ring = std::collections::VecDeque::new();
                while cyc < n * 62400 {
                    let f = cyc / 62400;
                    if let Some((k, until)) = down { if f >= until { tvc.key_up(k); down = None; } }
                    if down.is_none() && f >= next_key {
                        seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
                        let k = keys[((seed >> 33) % keys.len() as u64) as usize];
                        tvc.key_down(k); down = Some((k, f + 3));
                        next_key = f + [12u64, 20, 35][((seed >> 40) % 3) as usize];
                    }
                    let st = &tvc.z80.state; let (pc, sp) = (st.pc, st.sp);
                    if sp >= lo && sp < hi && sp < minsp { minsp = sp; }
                    ring.push_back(pc); if ring.len() > 64 { ring.pop_front(); }
                    let labels = tvc.bus.mmu.map_labels(); let page = (pc >> 14) as usize;
                    if labels[page].starts_with('U') && !(pc < 0x1A00 && page == 0) && !(pc >= 0x1A00 && pc < 0x8000) {
                        println!("ROSSZ PC={pc:04X} f{} {:?}", frame + f, ring); regs(&mut tvc); return;
                    }
                    if tvc.bus.mmu.r8(pc) == 0xED && tvc.bus.mmu.r8(pc.wrapping_add(1)) == 0x0F { println!("ED0F PC={pc:04X} {:?}", ring); return; }
                    cyc += tvc.debug_step_instruction() as u64;
                }
                frame += n;
                println!("fuzz kész, a lemezverem legmélyebb pontja: {minsp:04X} (teteje {hi:04X}, mélység {})", hi - minsp);
            }
            "watch" => {
                // utasításonként futtat n képkockányi ciklusig, és az utolsó 300 PC-t kiírja, ha a PC $1A00 alá vagy $8000 fölé (nem ROM) megy
                let n: u64 = arg.parse().unwrap();
                let mut ring = std::collections::VecDeque::new();
                let mut cyc: u64 = 0;
                while cyc < n * 62400 {
                    let pc = tvc.z80.state.pc; let map = tvc.bus.mmu.get_map_val();
                    let labels = tvc.bus.mmu.map_labels();
                    let page = (pc >> 14) as usize;
                    ring.push_back((pc, map, tvc.z80.state.sp));
                    if ring.len() > 300 { ring.pop_front(); }
                    let lab = labels[page];
                    let bad = (lab.starts_with('U') && !(page == 0 && pc < 0x1A00) && !(pc >= 0x1A00 && pc < 0x8000))
                        || (tvc.bus.mmu.r8(pc) == 0xED && tvc.bus.mmu.r8(pc.wrapping_add(1)) == 0x0F);
                    if bad {
                        println!("ROSSZ PC={pc:04X} lap={lab} map={map:02X}");
                        for (p, m, sp) in &ring { print!("{p:04X}/{m:02X}/{sp:04X} "); }
                        println!(); regs(&mut tvc); return;
                    }
                    cyc += tvc.debug_step_instruction() as u64;
                }
                frame += n;
            }
            "dumpu" => {
                // U0..U2 nyers tartalma fájlba (lapozástól független)
                let mut out = Vec::new();
                for b in ["U0", "U1", "U2"] { out.extend(tvc.bus.mmu.read_raw_bank(b, 0, 0x4000).unwrap()); }
                std::fs::write(arg, out).unwrap(); println!("dump {arg}");
            }
            "audio" => {
                // audio <fájl.wav> <képkocka>: a hang rögzítése
                let (f, n) = arg.split_once(' ').unwrap();
                let n: u64 = n.parse().unwrap();
                let mut samples: Vec<f32> = Vec::new();
                tvc.take_audio_samples();
                for _ in 0..n { tvc.run_for_a_frame(); frame += 1; samples.extend(tvc.take_audio_samples()); }
                let rate = tvc.sound_sample_rate();
                let mut w = std::fs::File::create(f).unwrap();
                let data_len = (samples.len() * 2) as u32;
                w.write_all(b"RIFF").unwrap(); w.write_all(&(36 + data_len).to_le_bytes()).unwrap();
                w.write_all(b"WAVEfmt ").unwrap(); w.write_all(&16u32.to_le_bytes()).unwrap();
                w.write_all(&1u16.to_le_bytes()).unwrap(); w.write_all(&1u16.to_le_bytes()).unwrap();
                w.write_all(&rate.to_le_bytes()).unwrap(); w.write_all(&(rate * 2).to_le_bytes()).unwrap();
                w.write_all(&2u16.to_le_bytes()).unwrap(); w.write_all(&16u16.to_le_bytes()).unwrap();
                w.write_all(b"data").unwrap(); w.write_all(&data_len.to_le_bytes()).unwrap();
                for s in samples { let v = (s.clamp(-1.0, 1.0) * 30000.0) as i16; w.write_all(&v.to_le_bytes()).unwrap(); }
                println!("audio {f} {rate} Hz");
            }
            "peek" => {
                let (ad, n) = arg.split_once(' ').unwrap();
                let ad = u16::from_str_radix(ad, 16).unwrap(); let n: u16 = n.parse().unwrap();
                print!("{ad:04X}:"); for i in 0..n { print!(" {:02X}", tvc.bus.mmu.r8(ad.wrapping_add(i))); } println!();
            }
            _ => panic!("ismeretlen parancs: {cmd}"),
        }
    }
}
