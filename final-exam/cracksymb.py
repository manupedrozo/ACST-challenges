import angr
import claripy

#Solve just like the example given in class
proj = angr.Project("./cracksymb")

chars = [claripy.BVS(f'c%d' % i, 8) for i in range(0x17)]
input_str = claripy.Concat(*chars + [claripy.BVV(b'\n')]) # + \n
initial_state = proj.factory.entry_state(stdin=input_str, add_options={angr.options.LAZY_SOLVES} ) # use as stdin

for c in chars: # make sure all chars are printable
    initial_state.solver.add(c >= 0x20, c <= 0x7e)

simgr = proj.factory.simulation_manager(initial_state)
simgr.explore(find=0x4033c2) # flag correct

if simgr.found:
    print(simgr.found[0].posix.dumps(0))

#flag{l1n34r_syst3ms_<3}
