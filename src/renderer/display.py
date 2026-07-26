import tkinter as tk

TAILLE_CASE = 20

def draw_square(new_img, col, ligne, valeur):
    """
    Draws a square on the image.
    """
    start = col * TAILLE_CASE
    inter = ligne * TAILLE_CASE
    # print(valeur)
    for i in range(TAILLE_CASE):
        for j in range(TAILLE_CASE):
            couleur = "black"
            if i == 0 and (valeur & 1):                       
                couleur = "blue"
            if i == TAILLE_CASE - 1 and (valeur & 4):       
                couleur = "blue"
            if j == 0 and (valeur & 8):              
                couleur = "blue"
            if j == TAILLE_CASE - 1 and (valeur & 2):   
                couleur = "blue"
            new_img.put(couleur, (start + j, inter + i))


def display_maze(maze: list[list[int]]) -> None:
    """
    Displays maze with tkinter.
    """
    root = tk.Tk()
    root.title("ᗧ Pac-Man ᗧ")

    new_img = tk.PhotoImage(width=500, height=500)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            draw_square(new_img, j, i, maze[i][j])
    tk.Label(root, image=new_img).pack()
    root.mainloop()