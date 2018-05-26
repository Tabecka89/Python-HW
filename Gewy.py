from unittest import *
from itertools import *
import ast
from tkinter import *
import re


def half(matrix, k=1):
    return [matrix[i][i:] if k is 0 else matrix[i][:i + 1] for i in range(len(matrix))]


def decrypt(string, key):
    new_str = ""
    for char in string:
        new_str += (chr((ord(char) + key - ord("a")) % (ord("z") - ord("a") + 1) + ord("a")))
    return new_str


def merge(iter1, iter2):
    iterator1 = iter(iter1)
    iterator2 = iter(iter2)
    x = next(iterator1, None)
    y = next(iterator2, None)
    while 1:
        if x is None and y is None:
            break
        elif x is None:
            yield y
            y = next(iterator2, None)
        elif y is None:
            yield x
            x = next(iterator1, None)
        elif x <= y:
            yield x
            x = next(iterator1, None)
        else:
            yield y
            y = next(iterator2, None)


def rank(file_name, how_to_rank='total'):
    mydict = dict()
    f = open(file_name, "r")
    for line in f:
        values = line.split()
        if how_to_rank == 'total':
            medal_value = int(values[1]) + int(values[2]) + int(values[3])
        elif how_to_rank == 'weighted':
            medal_value = int(values[1]) * 3 + int(values[2]) * 2 + int(values[3]) * 1
        elif how_to_rank == 'gold':
            medal_value = int(values[1])
        mydict[values[0]] = medal_value
    s = [(k, mydict[k]) for k in sorted(mydict, key=mydict.get, reverse=True)]
    for item, value in s:
        yield '"{}":{}'.format(item, value)


def test_half():
    matrix = [[1, 2, 3, 4, 5],
              [6, 7, 8, 9, "spam"],
              [11, 12, 13, 14, 15],
              [16, "stam", 18, 19, 20]]
    assert half(matrix, 1) == [[1], [6, 7], [11, 12, 13], [16, 'stam', 18, 19]]
    assert half(matrix, 0) == [[1, 2, 3, 4, 5], [7, 8, 9, 'spam'], [13, 14, 15], [19, 20]]
    assert half([], 1) == []


def test_decrypt():
    assert decrypt("plilkdxkaqexkhpcloqebcfpe", 3) == "solongandthanksforthefish"
    assert decrypt("zazaz", 1) == "ababa"


def test_merge():
    list1 = [1, 3, 7, 9]
    list2 = [2, 8, 12, 17, 22]
    assert list(merge(list1, list2)) == [1, 2, 3, 7, 8, 9, 12, 17, 22]
    assert list(merge([], [])) == []
    assert list(merge([1, 3, 5], [])) == [1, 3, 5]


def test_rank():
    for nation in rank('winners.txt', 'total'):
        print(nation)
    for nation in rank('winners.txt', 'weighted'):
        print(nation)
    for nation in rank('winners.txt', 'gold'):
        print(nation)


class Application:

    def __init__(self, master):
        self.master = master
        master.title("Questions")
        self.button_run1 = Button(master, text="Run Q1", command=lambda: self.create_window("Q1"))
        self.button_run2 = Button(master, text="Run Q2", command=lambda: self.create_window("Q2"))
        self.button_run3 = Button(master, text="Run Q3", command=lambda: self.create_window("Q3"))
        self.button_run4 = Button(master, text="Run Q4", command=lambda: self.create_window("Q4"))

        self.new_matrix = []

        # LAYOUT

        self.button_run1.grid(row=0, column=0)
        self.button_run2.grid(row=0, column=1)
        self.button_run3.grid(row=0, column=2)
        self.button_run4.grid(row=0, column=3)

    def create_window(self, method):
        if method == "Q1":
            self.create_window_q1()
        elif method == "Q2":
            self.create_window_q2()
        elif method == "Q3":
            self.create_window_q3()
        elif method == "Q4":
            self.create_window_q4()

    def create_window_q1(self):
        window_q1 = Toplevel(root)
        window_q1.title("Question 1")
        label_q1 = Label(window_q1, text="For a given matrix and K (0/1),\nthe function returns a matrix" \
                                         " which is cut halfway either from the top or bottom")
        label_q1.grid(row=0, column=0, columnspan=2)
        self.textbox = Text(window_q1, height=4, width=40)
        self.textbox.insert(END, str([[1, 2, 3, 4, 5],
                                      [6, 7, 8, 9, "spam"],
                                      [11, 12, 13, 14, 15],
                                      [16, "stam", 18, 19, 20]]))
        self.textbox.grid(row=1, column=0, columnspan=2)
        self.label_q1_k = Label(window_q1, text="K Value:")
        self.label_q1_k.grid(row=3, column=0, sticky=E)
        self.entry_q1_k = Entry(window_q1)
        self.entry_q1_k.insert(END, 1)
        self.entry_q1_k.grid(row=3, column=1, sticky=W)
        self.button_q1 = Button(window_q1, text="Run Q1", command=lambda: self.run_q1(
            "Q1", ast.literal_eval(self.textbox.get("1.0", 'end-1c')), int(self.entry_q1_k.get())))
        self.button_q1.grid(row=4, column=0, columnspan=2)

    def run_q1(self, method, matrix, k):
        if method == "Q1":
            self.new_matrix = half(matrix, k)
            self.textbox.delete('1.0', END)
            self.textbox.insert(END, str(self.new_matrix))
            self.entry_q1_k.delete(0, END)
            self.entry_q1_k.insert(END, k)


    def create_window_q2(self):
        default_string = "plilkdxkaqexkhpcloqebcfpe"
        window_q2 = Toplevel(root)
        window_q2.title("Question 2")
        label_q2 = Label(window_q2, text="For a given String and a decription key (>0),\n the function returns a decrypted secret message\n that holds the key for figuring out our place within the cosmos")
        label_q2.grid(row=0, column=0)
        label_string_prompt = Label(window_q2, text="Enter a String:")
        label_string_prompt.grid(row=1, column=0, sticky=W)
        label_key_prompt = Label(window_q2, text="Enter key(int>0):")
        label_key_prompt.grid(row=2, column=0, sticky=W)
        self.string_entry_q2 = Entry(window_q2, width=25)
        self.string_entry_q2.grid(row=1, column=0)
        self.string_entry_q2.insert(END, default_string)
        self.key_entry_q2 = Entry(window_q2, width=3)
        self.key_entry_q2.grid(row=2, column=0)
        self.key_entry_q2.insert(END, 3)
        label_q2_res = Label(window_q2, text="Decrypted:")
        label_q2_res.grid(row=4, column=0, sticky=W)
        self.button_q2 = Button(window_q2, text="Run Q2", command=lambda: self.run_q2("Q2", self.string_entry_q2.get(), int(self.key_entry_q2.get())))
        self.button_q2.grid(row=3, column=0)
        self.res_entry_q2 = Entry(window_q2, width=25)
        self.res_entry_q2.grid(row=4, column=0)

    def run_q2(self, method, string, key):
        self.res_entry_q2.delete(0, END)
        self.decrypted_string = decrypt(string, key)
        self.res_entry_q2.insert(0, self.decrypted_string)

    def create_window_q3(self):
        window_q3 = Toplevel(root)
        window_q3.title("Question 3")
        default_list_1 = [5, 101]
        default_list_2 = [1, 2]
        label_q3 = Label(window_q3, text="For 2 given sorted iterables, the function merges\n them like a FUCKING BOSS")
        label_q3.grid(row=0, column=0)
        label_prompt_q3 = Label(window_q3, text="Enter two ordered sequences of numbers:")
        self.first_iterable_entry = Entry(window_q3)
        self.second_iterable_entry = Entry(window_q3)
        self.first_iterable_entry.insert(END, default_list_1)
        self.second_iterable_entry.insert(END, default_list_2)
        self.button_q3 = Button(window_q3, text="Run Q3", command=lambda: self.run_q3(
            "Q3", self.first_iterable_entry.get(), self.second_iterable_entry.get()))
        self.res_entry_q3 = Entry(window_q3)
        label_prompt_q3.grid(row=1, column=0, sticky=W)
        self.first_iterable_entry.grid(row=1, column=1)
        self.second_iterable_entry.grid(row=1, column=2)
        self.button_q3.grid(row=2, column=1)
        self.res_entry_q3.grid(row=3, column=1)

    def run_q3(self, method, string1, string2):
        self.res_entry_q3.delete(0, END)
        iter1 = []
        iter2 = []
        string_list_1 = re.split(', |\s', string1)
        string_list_2 = re.split(', |\s', string2)
        for value in string_list_1:
            iter1.append(int(value))
        for value in string_list_2:
            iter2.append(int(value))
        res_list = []
        for x in merge(iter1, iter2):
            res_list.append(x)
        self.res_entry_q3.insert(0, res_list)

    def create_window_q4(self):
        window_q4 = Toplevel(root)
        window_q4.title("Question 4")

        how_to_rank = StringVar(root)
        Label(window_q4, text="File Name:").grid(row=1, column=0, sticky=E)
        file_name = Entry(window_q4)
        file_name.grid(row=1, column=1, sticky=W)
        file_name.insert(END, 'winners.txt')
        res_textbox = Text(window_q4, height=5, width=30)
        res_textbox.grid(row=0, column=2, rowspan=3)
        label_q3 = Label(window_q4, text="For a given text file that includes countries that won medals\n"
                                         "the function returns the countries ordered by the \n"
                                         "weight of the points they got.")
        label_q3.grid(row=0, column=0, columnspan=2)

        button_q4 = Button(window_q4, text="Run Q4", command=lambda: run_q4(file_name.get(), how_to_rank.get()))
        button_q4.grid(row=3, column=0, columnspan=2)
        # Dictionary with options
        choices = ['total', 'weighted', 'gold']
        how_to_rank.set('total')  # set the default option

        popup_menu = OptionMenu(window_q4, how_to_rank, *choices)
        Label(window_q4, text="How to rank:").grid(row=2, column=0, sticky=E)
        popup_menu.grid(row=2, column=1, sticky=W)

        # on change dropdown value
        def change_dropdown(*args):
            print(how_to_rank.get())

        # link function to change dropdown
        how_to_rank.trace('w', change_dropdown)

        def run_q4(f_name, to_rank):
            res_textbox.delete('1.0', END)
            for nation in rank(f_name, to_rank):
                res_textbox.insert(END, nation)
                res_textbox.insert(END, '\n')


if __name__ == "__main__":
    test_half()
    test_decrypt()
    test_merge()
   # test_rank()
    root = Tk()
    my_gui = Application(root)
    root.mainloop()
    print("done testing")
