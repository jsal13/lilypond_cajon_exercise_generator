nam = \lyricmode { bass snare hihat ride }
mus = \drummode { bd sn hh cymr }
\score {
  << \new DrumStaff \with {
       \remove Bar_engraver
       \remove Time_signature_engraver
       \hide Stem
       \override Stem.Y-extent = ##f
     } \mus
     \new Lyrics \nam
  >>
  \layout {
    \context {
      \Score
    }
  }
}