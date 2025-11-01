import tkinter as tk
from tkinter import messagebox
import pandas as pd

# -----------------------------
# Algorithm Implementations
# -----------------------------

# Quick Sort (recursive)
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr)//2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)

# Binary Search (returns all indices where target appears)
def binary_search_all(arr, target):
    low, high = 0, len(arr) - 1
    found_indices = []

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            # Found one occurrence — expand left & right to find all
            left = mid
            while left >= 0 and arr[left] == target:
                if left not in found_indices:
                    found_indices.append(left)
                left -= 1
            right = mid + 1
            while right < len(arr) and arr[right] == target:
                if right not in found_indices:
                    found_indices.append(right)
                right += 1
            break
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return sorted(found_indices)  # empty if not found

# -----------------------------
# Tkinter GUI Functions
# -----------------------------

def parse_array_input(text):
    tokens = text.split(',')
    arr = []
    for t in tokens:
        s = t.strip()
        if s == '':
            continue
        try:
            num = int(s)
            arr.append(num)
        except ValueError:
            continue
    return arr

def perform_operation():
    try:
        # Parse user array input
        user_input = entry_array.get()
        arr = parse_array_input(user_input)
        if not arr:
            messagebox.showerror("Error", "Please enter a valid numeric array (comma-separated integers).")
            return

        operation = operation_var.get()

        # ---------------- Sorting ----------------
        if operation == "Sort":
            sorted_arr = quick_sort(arr)
            df = pd.DataFrame(sorted_arr, columns=["Sorted Array"])
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "✅ Sorted Array (Quick Sort):\n\n")
            output_text.insert(tk.END, df.to_string(index=True))

        # ---------------- Searching (Binary Search) ----------------
        elif operation == "Search":
            search_val_raw = entry_search.get().strip()
            if search_val_raw == "":
                messagebox.showerror("Error", "Please enter a value to search.")
                return
            try:
                search_val = int(search_val_raw)
            except ValueError:
                messagebox.showerror("Error", "Search value must be an integer.")
                return

            # Sort array for binary search
            sorted_arr = quick_sort(arr)

            # Perform binary search for all occurrences
            indices = binary_search_all(sorted_arr, search_val)

            output_text.delete(1.0, tk.END)
            if indices:
                index_list = ', '.join(map(str, indices))
                output_text.insert(tk.END, f"✅ Element {search_val} found at index/indices: {index_list}")
            else:
                output_text.insert(tk.END, f"❌ Element {search_val} not found in the array.")

        else:
            messagebox.showerror("Error", "Please select an operation (Sort or Search).")

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

def toggle_search_entry():
    if operation_var.get() == "Search":
        entry_search.config(state="normal")
    else:
        entry_search.config(state="disabled")

# -----------------------------
# Tkinter GUI Layout
# -----------------------------

root = tk.Tk()
root.title("Array Sorting and Binary Search Tool")
root.geometry("620x480")
root.config(bg="#F2F2F2")

message = tk.Label(root, text="Array Sorter and Binary Search Tool", fg='green', font=("Arial", 16, "bold"))
message.pack(pady=8)

# Input label and entry
tk.Label(root, text="Enter Array (comma-separated integers):", bg="#F2F2F2", font=("Arial", 12)).pack(pady=8)
entry_array = tk.Entry(root, width=70)
entry_array.pack(pady=5)

# Operation selection
operation_var = tk.StringVar()
tk.Label(root, text="Choose Operation:", bg="#F2F2F2", font=("Arial", 12)).pack(pady=6)
tk.Radiobutton(root, text="Sorting (Quick Sort)", variable=operation_var, value="Sort",
               command=toggle_search_entry, bg="#F2F2F2").pack()
tk.Radiobutton(root, text="Searching (Binary Search)", variable=operation_var, value="Search",
               command=toggle_search_entry, bg="#F2F2F2").pack()

# Search entry (disabled initially)
tk.Label(root, text="Enter Element to Search (integer):", bg="#F2F2F2", font=("Arial", 12)).pack(pady=6)
entry_search = tk.Entry(root, width=30, state="disabled")
entry_search.pack(pady=5)

# Button to perform operation
tk.Button(root, text="Perform Operation", command=perform_operation,
          bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=12)

# Output box
tk.Label(root, text="Output:", bg="#F2F2F2", font=("Arial", 12)).pack()
output_text = tk.Text(root, height=12, width=70)
output_text.pack(pady=8)

# Set default operation
operation_var.set("Sort")

root.mainloop()
