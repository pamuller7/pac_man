from mazegenerator import MazeGenerator

m_cl = MazeGenerator(size=(15, 15),
                     perfect=False,
                     entry_cell=(0, 0),
                     exit_cell=(-1, -1))
print(m_cl.maze)
m_cl.generate()
print("\n\n")
for maze in m_cl.maze:
    for cell in maze:
        print(bin(cell), end=" ")

    print()
print("\n")
print(m_cl.shortest_path)
