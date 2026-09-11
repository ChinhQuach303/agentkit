# Smell Baseline (disclosed reference for `review`)

Fowler smells (*Refactoring*, ch.3), fixed set that applies even when a repo documents nothing. Each reads *what it is* → *fix*. Two rules bind it: **the repo overrides** (a documented standard wins; suppress the smell where endorsed) and **always a judgement call** (label "possible X", never a hard violation; skip anything tooling enforces).

- **Mysterious Name**: name hides what it does/holds. → rename; no honest name = murky design.
- **Duplicated Code**: same logic shape in >1 hunk/file. → extract, call from both.
- **Feature Envy**: method reaches into another object's data more than its own. → move it onto the envied data.
- **Data Clumps**: same fields/params travelling together (a type wanting birth). → bundle into one type.
- **Primitive Obsession**: primitive standing in for a domain concept. → small dedicated type.
- **Repeated Switches**: same `switch`/`if`-cascade on one type recurring. → polymorphism, or one shared map.
- **Shotgun Surgery**: one logical change scatters edits across files. → gather changers-together into one module.
- **Divergent Change**: one file edited for unrelated reasons. → split per reason.
- **Speculative Generality**: abstraction/hooks for needs the spec lacks. → delete; inline until a real need shows.
- **Message Chains**: long `a.b().c()` walks the caller shouldn't depend on. → hide behind one method.
- **Middle Man**: class/function mostly delegating onward. → cut, call direct.
- **Refused Bequest**: subclass ignoring most of its inheritance. → composition over inheritance.
