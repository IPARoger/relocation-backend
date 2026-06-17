# Relay governance folder

Drop or symlink your binding `.md` files here. The robot reads every `*.md`
in this folder (except this README) and sends them to the planner API — the
same role as pasting discipline into Claude by hand.

No separate instructions file needed. Move or link existing docs, e.g.:

    ln -s ../../docs/architecture/TWO_AGENT_RELAY_GOVERNANCE.md .
    ln -s ../../docs/architecture/ARCHITECTURE_AND_BACKEND_CANON.md .

Files are included in name order. Keep the set focused; very large folders
increase planner API cost slightly (see relay_robot.py header).
