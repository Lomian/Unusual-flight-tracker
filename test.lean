def turnDiff (a b : Int) : Int :=
  Int.natAbs (((a - b + 180) % 360) - 180)

#eval turnDiff 350 10   -- 20
#eval turnDiff 10 350   -- 20
#eval turnDiff 90 270   -- 180
#eval turnDiff 45 45    -- 0
