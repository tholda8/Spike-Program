# Star Wars Main Theme - Main Melody Line (Arranged at ~120 BPM)
# Quarter note = 500ms, Eighth note = 250ms, Dotted Half = 1500ms
star_wars_theme = [
    # Measure 1: Introductory Triplet
    (294, 166), (294, 166), (294, 166), # D4 (Triplet Eighths)
    
    # Measure 2
    (392, 1500),                         # G4 (Dotted Half)
    (587, 500),                          # D5 (Quarter note)
    
    # Measure 3
    (523, 250),                          # C5 (Eighth note)
    (494, 250),                          # B4 (Eighth note)
    (440, 250),                          # A4 (Eighth note)
    (784, 1000),                         # G5 (Half note)
    (587, 500),                          # D5 (Quarter note)
    
    # Measure 4
    (523, 250),                          # C5 (Eighth note)
    (494, 250),                          # B4 (Eighth note)
    (440, 250),                          # A4 (Eighth note)
    (784, 1000),                         # G5 (Half note)
    (587, 500),                          # D5 (Quarter note)
    
    # Measure 5
    (523, 250),                          # C5 (Eighth note)
    (494, 250),                          # B4 (Eighth note)
    (523, 250),                          # C5 (Eighth note)
    (440, 1000),                         # A4 (Half note)
    (294, 250),                          # D4 (Eighth note)
    (294, 250),                          # D4 (Eighth note)
    
    # Measure 6: Return to main theme note
    (392, 1500),                          # G4 (Dotted Half)

    # Takt 17-18: B sekce motivu
    (587, 500),                          # D5 (Čtvrťová)
    (392, 250), (392, 250), (392, 250),  # G4 (Osminky)
    (523, 500),                          # C5 (Čtvrťová)
    (494, 250), (440, 250),              # B4, A4 (Osminky)
    (784, 500),                          # G5 (Čtvrťová)
    (587, 500),                          # D5 (Čtvrťová)

    # Takt 19-20
    (523, 250), (494, 250), (440, 250),  # C5, B4, A4 (Osminky)
    (784, 1000),                         # G5 (Půlová)
    (587, 500),                          # D5 (Čtvrťová)
    (523, 250), (494, 250), (523, 250),  # C5, B4, C5 (Osminky)
    (440, 1000),                         # A4 (Půlová)

    # Takt 21-22: Dramatický přechod s alterovanými tóny
    (294, 250), (294, 250),              # D4, D4 (Osminky)
    (440, 750),                          # A4 (Tečkovaná čtvrťová)
    (440, 250),                          # A4 (Osminka)
    (523, 250), (494, 250), (440, 250),  # C5, B4, A4 (Osminky)
    (392, 250),                          # G4 (Osminka)
    (392, 1000),                         # G4 (Půlová)

    # Takt 23-24
    (440, 250), (494, 250),              # A4, B4 (Osminky)
    (523, 500),                          # C5 (Čtvrťová)
    (440, 250),                          # A4 (Osminka)
    (494, 250),                          # B4 (Osminka)
    (587, 500),                          # D5 (Čtvrťová)
    (440, 250),                          # A4 (Osminka)
    (494, 250),                          # B4 (Osminka)

    # Takt 25-26: Vyvrcholení na vysoké tóny
    (659, 750),                          # E5 (Tečkovaná čtvrťová)
    (587, 250),                          # D5 (Osminka)
    (698, 500),                          # F5 (Čtvrťová)
    (587, 250), (698, 250),              # D5, F5 (Osminky)
    (880, 1500),                         # A5 (Tečkovaná půlová)

    # Takt 27-28: Finální akcenty a závěr
    (587, 500),                          # D5 (Čtvrťová)
    (294, 166), (294, 166), (294, 166),  # D4 (Triola)
    (392, 1000),                         # G4 (Půlová akordická)
    (0, 500)                             # Pauza (Konec)
]
