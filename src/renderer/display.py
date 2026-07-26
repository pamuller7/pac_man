import tkinter as tk




def display_maze(maze: list[list[int]]) -> None:
    """
    Displays maze with tkinter.
    """
    root = tk.Tk()
    root.title("ᗧ Pac-Man ᗧ")
    square_location_x = 40
    square_location_y = 0

    new_img = tk.PhotoImage(width=500, height=500)
    for i in range(50):
        for j in range(50):
            new_img.put("blue", (square_location_x + j, square_location_y + i))
    for x in range(50):
        new_img.put("#FF0000", (square_location_x + x, square_location_y))
    tk.Label(root, image=new_img).pack()
    root.mainloop()