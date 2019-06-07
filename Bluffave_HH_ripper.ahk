#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
^1::
sleep, 0000
Loop, 140{
MouseMove, 0, -65, 50, R
sleep, 60
Click
sleep, 60
Send, {Ctrl Down}a{Ctrl up}
sleep, 60
Send, {Ctrl Down}c{Ctrl up}
sleep, 60
MouseMove, 820, -605, 50, R
sleep, 60
Click
sleep, 60
Send, {Ctrl Down}v{Ctrl up}
sleep, 60
MouseMove, -820, 670, 50, R
sleep, 60
Click
sleep, 60
}
Return

^l::
	ExitApp

;pref pos: Rahul->Phil->Hardy->Nicholas->Ali->Pandu->Dwan
;Ali: limpcalls a bunch, raisespre are strong donk flop/turn is generally TPTK+.
;bets small for value a bunch? YES! big donk flop is like MP
;Ayush: too limp/cally. Raises pre polarized to 72 or nuts. exact river PSB is junk. 1/2pot riv psb is med good.
;Phil: cbetsF/T too much, donk is like middling+ value
;2bet flop is 1.53, so value only...
;Dwan: on the station side pre, post is not a much of a station (will fuck you)
;Rahul: watch the special sizings for strength tells. Too value heavy. Always bluff opens a post.
;Hardy: a tight player in general. Steal and fold to 3b, fast call strong leak? 2bets flop with ONLY VALUE. ;x flop or x back flop leaves his range super weak
;Pandu: postflop big overbet raise is far stronger than weaker minraise. Turn raises if bigish are nutted.
;Victor: AGGRO FISH overstabs FTR, call light, cannot be bluffed
;A: minbet is weak value lol