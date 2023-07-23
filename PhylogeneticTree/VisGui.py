import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

## GLOBAL VARIABLES

## NCBI

## SA

## MSA

msa_filePath = None  # for choose a file
msa_sequence = None  # for pasting
msa_algorithm = None
msa_output_file_name = None  # esm el file eli han use ba3d kda 3shan n output feeh

## TREE
tree_filePath = None  # for choose a file option
tree_aligned_sequence = None  # for paste a sequence option
tree_output_file_name = None  # the output file after running the phyml


def center_window(window, width, height):
  window.update_idletasks()
  x = (window.winfo_screenwidth() - width) // 2
  y = (window.winfo_screenheight() - height) // 2
  window.geometry(f"{width}x{height}+{x}+{y}")


def show_selected():
  selected_option = var.get()
  if selected_option in [1, 2, 3, 4]:
    if selected_option == 1:
      page_of_ncbi()
    elif selected_option == 2:
      page_of_sq_al()
    elif selected_option == 3:
      page_of_msa()
    else:
      page_of_tree()
  else:
    messagebox.showwarning("Error", "Please select an option.")


def show_message(title, message):
  error_dialog = tk.Toplevel(root)
  error_dialog.title(title)
  error_dialog.config(bg='white')

  error_label = tk.Label(error_dialog,
                         text=message,
                         bg='white',
                         font=("Helvetica", 16),
                         wraplength=500)
  error_label.pack(pady=20)

  ok_button = tk.Button(error_dialog,
                        text="OK",
                        command=error_dialog.destroy,
                        font=("Helvetica", 14))
  ok_button.pack(pady=10)

  center_window(error_dialog, 600, 300)  # Adjust the dialog size as needed


def page_of_ncbi():
  new_window = tk.Toplevel(root)
  new_window.title("Get Data from NCBI")
  new_window.config(bg='white')
  new_label = tk.Label(new_window,
                       text="Congratulations! You are on the new page.",
                       bg='white',
                       font=("Helvetica", 16))
  new_label.pack()
  center_window(new_window, 400, 200)
  new_window.attributes("-zoomed", True)


def page_of_sq_al():
  new_window = tk.Toplevel(root)
  new_window.title("Sequence Alignment")
  new_window.config(bg='white')
  new_label = tk.Label(new_window,
                       text="Congratulations! You are on the new page.",
                       bg='white',
                       font=("Helvetica", 16))
  new_label.pack()
  center_window(new_window, 400, 200)
  new_window.attributes("-zoomed", True)


##### MSA


def page_of_msa():
  global msa_output_file_name, msa_sequence, msa_filePath
  msa_sequence = None
  msa_filePath = None

  def open_file_explorer():
    global msa_filePath, msa_sequence
    msa_algorithm = var_msa.get()
    if msa_algorithm:
      msa_filePath = filedialog.askopenfilename(filetypes=[("All Files",
                                                            "*.*")])
      msa_sequence = None  # Reset msa_sequence when choosing a file
    else:
      show_message("MSA Algorithm is Not Chosen",
                   "Please choose an MSA algorithm before selecting a file.")

  def paste_sequence():
    global msa_sequence, msa_filePath
    msa_algorithm = var_msa.get()
    if msa_algorithm:

      def save_sequence():
        global msa_sequence, msa_filePath
        sequence = text_box.get("1.0", "end-1c")
        if sequence.strip():
          msa_sequence = sequence
          msa_filePath = None  # Reset msa_filePath when pasting a sequence
          sequence_dialog.destroy()
        else:
          show_message("Empty Sequence", "Please enter a sequence!")

      sequence_dialog = tk.Toplevel(new_window)
      sequence_dialog.title("Paste a Sequence")
      sequence_dialog.config(bg='white')

      text_label = tk.Label(sequence_dialog,
                            text="Paste your sequence below:",
                            bg='white',
                            font=("Helvetica", 12))
      text_label.pack(pady=10)

      text_box = tk.Text(sequence_dialog, width=40, height=10)
      text_box.pack()

      save_button = tk.Button(sequence_dialog,
                              text="Save Sequence",
                              command=save_sequence,
                              font=("Helvetica", 16))
      save_button.pack(pady=10)

      center_window(sequence_dialog, 600, 400)
    else:
      show_message(
        "MSA Algorithm is Not Chosen",
        "Please choose an MSA algorithm before pasting a sequence.")

  def exit_page():
    new_window.destroy()

  def run_algorithm():
    global msa_output_file_name  # Use the global variable for output_text
    output_file_name = msa_output_file_name.get()
    if output_file_name.strip():
      output_file_name = output_file_name
      msa_algorithm = var_msa.get()
      print(
        f'Running {msa_algorithm} algorithm, on {msa_filePath} or {msa_sequence}, saving it in {output_file_name}'
      )
      # Prepare the MSA command based on the chosen options
      if msa_filePath:
        if msa_algorithm == "clustal":
          msa_command = f"./MSA.sh -msaTool clo -outName {output_file_name} -seqPath {msa_filePath}"
        else:
          msa_command = f"./MSA.sh -msaTool mft -outName {output_file_name} -seqPath {msa_filePath}"
      else:
        if msa_algorithm == "clustal":
          msa_command = f"./MSA.sh -msaTool clo -outName {output_file_name} -seqPaste <<EOF\n{msa_sequence}\nEOF"
        else:
          msa_command = f"./MSA.sh -msaTool mft -outName {output_file_name} -seqPaste <<EOF\n{msa_sequence}\nEOF"

      # Run the MSA script using subprocess
      try:
        subprocess.run(msa_command, shell=True, check=True)
      except subprocess.CalledProcessError:
        show_message("MSA Execution Error",
                     "An error occurred while running the MSA script.")
        return

      # Optionally, display a success message
      show_message("MSA Completed", msa_command)

    else:
      show_message("Output File Name Missing",
                   "Please enter a valid output file name.")

  def check_msa_option():
    msa_algorithm = var_msa.get()
    if msa_sequence is not None:
      return True
    else:
      return False

  new_window = tk.Toplevel(root)
  new_window.title("Multiple Sequence Alignment")
  new_window.config(bg='white')

  new_label = tk.Label(
    new_window,
    text=
    "To run MSA, choose the algorithm (Clustal Omega or MAFFT), (choose a file or paste the sequence), type the output file name, finally press on Run Algorithm",
    bg='white',
    font=("Helvetica", 16))
  new_label.pack(pady=20)

  var_msa = tk.StringVar()

  radio_button_clustal = tk.Radiobutton(new_window,
                                        text="Clustal Omega",
                                        variable=var_msa,
                                        value="clustal",
                                        bg='white',
                                        font=("Helvetica", 14))
  radio_button_clustal.pack(padx=10, pady=5)

  radio_button_mafft = tk.Radiobutton(new_window,
                                      text="MAFFT",
                                      variable=var_msa,
                                      value="mafft",
                                      bg='white',
                                      font=("Helvetica", 14))
  radio_button_mafft.pack(padx=10, pady=5)

  button_frame = tk.Frame(new_window, bg='white')
  button_frame.pack()

  choose_file_button = tk.Button(
    button_frame,
    text="Choose a File",
    command=lambda: [check_msa_option(),
                     open_file_explorer()],
    font=("Helvetica", 16))
  choose_file_button.pack(side=tk.LEFT, padx=10, pady=10)

  paste_sequence_button = tk.Button(
    button_frame,
    text="Paste a Sequence",
    command=lambda: [check_msa_option(), paste_sequence()],
    font=("Helvetica", 16))
  paste_sequence_button.pack(side=tk.LEFT, padx=10, pady=10)

  output_label = tk.Label(new_window,
                          text="Output File Name:",
                          bg='white',
                          font=("Helvetica", 14))
  output_label.pack(pady=5)

  msa_output_file_name = tk.Entry(new_window, font=("Helvetica", 12))
  msa_output_file_name.pack(pady=5)

  run_button = tk.Button(new_window,
                         text="Run Algorithm",
                         command=run_algorithm,
                         font=("Helvetica", 16))
  run_button.pack(pady=10)

  exit_button = tk.Button(new_window,
                          text="Exit",
                          command=exit_page,
                          font=("Helvetica", 16))
  exit_button.pack(pady=10)

  center_window(new_window, 600, 500)
  new_window.attributes("-zoomed", True)


######## Jehad code asli
# def page_of_tree2(): # yb2a ems7i 2
#   new_window = tk.Toplevel(root)
#   new_window.title("Phylogenetic Tree")
#   new_window.config(bg='white')
#   new_label = tk.Label(new_window,
#                        text="Congratulations! You are on the new page.",
#                        bg='white',
#                        font=("Helvetica", 16))
#   new_label.pack()
#   center_window(new_window, 400, 200)
#   new_window.attributes("-zoomed", True)


########## added code bet3 tawfik 3shan a3ml zayo
def page_of_tree():
  global tree_output_file_name, tree_aligned_sequence, tree_filePath

  tree_aligned_sequence = None
  tree_filePath = None

  def tree_open_file_explorer():  # in case user selected Choose a File option
    global tree_filePath, tree_aligned_sequence
    #msa_algorithm = var_tree.get() # here
    #if msa_algorithm:
    tree_filePath = filedialog.askopenfilename(filetypes=[("All Files",
                                                           "*.*")])
    tree_aligned_sequence = None  # Reset tree_aligned_sequence when choosing a file
    #else:
    #show_message("MSA Algorithm is Not Chosen", "Please choose an MSA algorithm before selecting a file.")

  # def tree_paste_sequence(
  # ):  # in case user selected Paste an Aligned Sequence option
  #   global tree_aligned_sequence, tree_filePath

    #msa_algorithm = var_tree.get()
    #if msa_algorithm:
    # def tree_save_sequence():
    #   global tree_aligned_sequence, tree_filePath
    #   sequence = text_box.get("1.0", "end-1c")
    #   if sequence.strip():
    #     tree_aligned_sequence = sequence
    #     tree_filePath = None  # Reset tree_filePath when pasting a sequence
    #     sequence_dialog.destroy()
    #   else:
    #     show_message("Empty Sequence", "Please enter a sequence!")

    # sequence_dialog = tk.Toplevel(new_window)
    # sequence_dialog.title("Paste an Aligned Sequence")
    # sequence_dialog.config(bg='white')

    # text_label = tk.Label(sequence_dialog,
    #                       text="Paste your aligned sequence below:",
    #                       bg='green',
    #                       font=("Helvetica", 12))
    # text_label.pack(pady=10)

    # text_box = tk.Text(sequence_dialog, width=40, height=10)
    # text_box.pack()

    # save_button = tk.Button(sequence_dialog,
    #                         text="Save Sequence",
    #                         command=tree_save_sequence,
    #                         font=("Helvetica", 16))
    # save_button.pack(pady=10)

    # center_window(sequence_dialog, 600, 400)
    #else:
    #show_message("MSA Algorithm is Not Chosen", "Please choose an MSA algorithm before pasting a sequence.")

  def tree_run_algorithm():
    global tree_output_file_name  # Use the global variable for output_text
    #output_file_name = tree_output_file_name.get()
    #if output_file_name.strip():
    #output_file_name = output_file_name
    #msa_algorithm = var_tree.get()
    #print(f'Running {msa_algorithm} algorithm, on {msa_filePath} or {msa_sequence}, saving it in {output_file_name}')
    # Prepare the Tree command based on the chosen options
    if tree_filePath:
      #if msa_algorithm == "clustal":
      #./PHYLO.sh --inName trialsequence.msa.fasta
      tree_command = f"./PHYLO.sh --inName {tree_filePath}"
      #else:
      #msa_command = f"./MSA.sh -msaTool mft -outName {output_file_name} -seqPath {msa_filePath}"
      #else:
      #if msa_algorithm == "clustal":
      # tree_command = f"./PhyTree.sh -msaTool clo -outName {output_file_name} -seqPaste <<EOF\n{msa_sequence}\nEOF"
      #else:
      #tree_command = f"./MSA.sh -msaTool mft -outName {output_file_name} -seqPaste <<EOF\n{msa_sequence}\nEOF"

      # Run the MSA script using subprocess
    try:
      subprocess.run(tree_command, shell=True, check=True)
    except subprocess.CalledProcessError:
      show_message("Tree Execution Error",
                   "An error occurred while running the Tree script.")
    return

  
  def tree_visualize():
    tree_command = "python3 TreeVis.py aseq.refined.phylip_phyml_tree.txt"
    try:
      subprocess.run(tree_command, shell=True, check=True)
    except subprocess.CalledProcessError:
      show_message(
        "Visualization Execution Error",
        "An error occurred while running the Visualization script.")
    return
    
    # Optionally, display a success message
    show_message("Tree Completed", tree_command)

  
  def exit_page():
    new_window.destroy()
    #else:
    #show_message("Output File Name Missing",
    #            "Please enter a valid output file name.")

  # def check_tree_option():
  #   #msa_algorithm = var_tree.get()
  #   if tree_aligned_sequence is not None:
  #     return True
  #   else:
  #     return False

  new_window = tk.Toplevel(root)
  new_window.title("Phylogenetic Tree Construction")
  new_window.config(bg='white')

  new_label = tk.Label(
    new_window,
    text=
    "To run Phylogenetic Tree:\n 1- Input the Aligned Sequence by selecting Choose a File\n 2- Press on Run Tree\n 3- Finally, output the tree visualization",
    fg='black',
    font=("Helvetica", 14))
  new_label.pack(pady=20)

  # image_file = "tree.png"
  # image1 = tk.PhotoImage(file=image_file)
  # image1 = image1.subsample(6, 6)

# Create a label with the image
  # image_label = tk.Label(new_window, image=image1, bg='white')
  # image_label.pack(pady=10)
  # # Create a button with the image as the background
  # button = tk.Button(root, image=image, text="Click me!")
  # button.pack(padx=10, pady=10)


  #var_tree = tk.StringVar()

  #radio_button_clustal = tk.Radiobutton(new_window, text="Clustal Omega", variable=var_tree, value="clustal", bg='white', font=("Helvetica", 14))
  #radio_button_clustal.pack(padx=10, pady=5)

  #radio_button_mafft = tk.Radiobutton(new_window, text="MAFFT", variable=var_tree, value="mafft", bg='white', font=("Helvetica", 14))
  #radio_button_mafft.pack(padx=10, pady=5)

  button_frame = tk.Frame(new_window, bg='white')
  button_frame.pack()

  choose_file_button = tk.Button(
    button_frame,
    text="1. Choose a File",
    fg='green',
    command=lambda: [#check_tree_option(),
                     tree_open_file_explorer()],
    font=("Arial", 14))
  choose_file_button.pack(side=tk.LEFT, padx=15, pady=30)

  # visualize_button = tk.Button(
  #   button_frame,
  #   text="Visualize Tree",
  #   command=lambda: [check_tree_option(),
  #                    tree_paste_sequence()],
  #   font=("Helvetica", 16))
  # visualize_button.pack(side=tk.LEFT, padx=10, pady=10)

  # output_label = tk.Label(new_window,
  #                        text="Output File Name:",
  #                       bg='white',
  #                      font=("Helvetica", 14))
  #output_label.pack(pady=5)

  #tree_output_file_name = tk.Entry(new_window, font=("Helvetica", 12))
  #tree_output_file_name.pack(pady=5)

  run_button = tk.Button(button_frame,
                         text="2. Run Tree",
                         fg='green',
                         command=tree_run_algorithm,
                         font=("Arial", 14))
  run_button.pack(side=tk.LEFT, padx=15, pady=30)

  visualize_button = tk.Button(button_frame,
                               text="3. Visualize Tree",
                               fg='green',
                               command=tree_visualize,
                               font=("Arial", 14))
  visualize_button.pack(side=tk.LEFT, padx=15, pady=30)

  
  # tree_label = tk.Button(button_frame,
  #                       image=image1,
  #                       text="Tree",
  #                       bg='white',
  #                       font=("Helvetica", 8))
  # tree_label.pack(padx=10, pady=10)

  exit_button = tk.Button(new_window,
                          text="Exit",
                          fg='red',
                          command=exit_page,
                          font=("Arial", 12))
  exit_button.pack(pady=20)

  center_window(new_window, 600, 500)
  new_window.attributes("-zoomed", True)


################## akhri hena

# Create the root window
root = tk.Tk()
root.title("Bioinformatics Automation Script - NU")

# Set the background color to white
root.configure(bg='white')

# Maximize the window at the beginning
root.attributes("-zoomed", True)

# Create a 2x2 grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

var = tk.IntVar()

image_file = "nu.png"
image = tk.PhotoImage(file=image_file)

# Create a button with the image as the background
#button = tk.Button(root, image=image, text="Click me!")
#button.pack(padx=10, pady=10)

welcome_label = tk.Label(root,
                         image=image,
                         text="Course Project - Spring 2023",
                         bg='white',
                         font=("Helvetica", 16))
welcome_label.grid(row=0, column=0, columnspan=2, pady=(10, 10))

option1 = tk.Radiobutton(root,
                         text="Get Data from NCBI",
                         variable=var,
                         value=1,
                         bg='white',
                         font=("Helvetica", 14),
                         wraplength=180)
option2 = tk.Radiobutton(root,
                         text="Sequence Alignment",
                         variable=var,
                         value=2,
                         bg='white',
                         font=("Helvetica", 14),
                         wraplength=180)
option3 = tk.Radiobutton(root,
                         text="Multiple Sequence Alignment",
                         variable=var,
                         value=3,
                         bg='white',
                         font=("Helvetica", 14),
                         wraplength=180)
option4 = tk.Radiobutton(root,
                         text="Phylogenetic Tree",
                         variable=var,
                         value=4,
                         bg='white',
                         font=("Helvetica", 14),
                         wraplength=180)

option1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
option2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
option3.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
option4.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

continue_button = tk.Button(root,
                            text="Continue",
                            command=show_selected,
                            font=("Helvetica", 14))
continue_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
