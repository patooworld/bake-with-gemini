import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Here's a Python function that sorts a list of numbers in ascending order. Identify the time complexity of this function. Then optimize this function and explain why it is faster. Don't use Python's in-built sort() method.\n\n\n```def sort_list(list_to_sort):\n  \"\"\"\n  This function sorts a list of numbers in ascending order using the bubble sort algorithm.\n\n  Args:\n    list_to_sort: A list of numbers to be sorted.\n\n  Returns:\n    A new list with the numbers sorted in ascending order.\n  \"\"\"\n  # Create a copy of the list to avoid modifying the original\n  sorted_list = list_to_sort.copy()\n  n = len(sorted_list)\n\n  # Iterate through the list n-1 times\n  for i in range(n-1):\n    # Flag to track if any swaps were made in a pass\n    swapped = False\n    # Iterate through the unsorted portion of the list\n    for j in range(n-i-1):\n      # Compare adjacent elements and swap if necessary\n      if sorted_list[j] > sorted_list[j+1]:\n        sorted_list[j], sorted_list[j+1] = sorted_list[j+1], sorted_list[j]\n        swapped = True\n    # If no swaps were made, the list is already sorted\n    if not swapped:\n      break\n\n  # Return the sorted list\n  return sorted_list\n\n# Example usage\nmy_list = [1, 9, 5, 2, 1, 8, 6, 6, 3, 4, 10, 7]\nsorted_list = sort_list(my_list)\nprint(sorted_list)  # Output: [1, 1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10]\n```",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```python\ndef sort_list(list_to_sort):\n  \"\"\"\n  This function sorts a list of numbers in ascending order using the bubble sort algorithm.\n\n  Args:\n    list_to_sort: A list of numbers to be sorted.\n\n  Returns:\n    A new list with the numbers sorted in ascending order.\n  \"\"\"\n  # Create a copy of the list to avoid modifying the original\n  sorted_list = list_to_sort.copy()\n  n = len(sorted_list)\n\n  # Iterate through the list n-1 times\n  for i in range(n-1):\n    # Flag to track if any swaps were made in a pass\n    swapped = False\n    # Iterate through the unsorted portion of the list\n    for j in range(n-i-1):\n      # Compare adjacent elements and swap if necessary\n      if sorted_list[j] > sorted_list[j+1]:\n        sorted_list[j], sorted_list[j+1] = sorted_list[j+1], sorted_list[j]\n        swapped = True\n    # If no swaps were made, the list is already sorted\n    if not swapped:\n      break\n\n  # Return the sorted list\n  return sorted_list\n\n# Example usage\nmy_list = [1, 9, 5, 2, 1, 8, 6, 6, 3, 4, 10, 7]\nsorted_list = sort_list(my_list)\nprint(sorted_list)  # Output: [1, 1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10]\n```\n\n**Time Complexity of Bubble Sort:**\n\nThe provided function uses the bubble sort algorithm. Bubble sort has a time complexity of **O(n^2)** in the worst and average case, where 'n' is the number of elements in the list. \n\n**Explanation:**\n\n* The outer loop iterates n-1 times.\n* The inner loop iterates through the unsorted portion of the list, which is also roughly 'n' in the worst case.\n* This nested loop structure results in O(n * n) = O(n^2) operations.\n\n**Optimized Function (Insertion Sort):**\n\n```python\ndef insertion_sort(list_to_sort):\n  \"\"\"\n  This function sorts a list of numbers in ascending order using the insertion sort algorithm.\n\n  Args:\n    list_to_sort: A list of numbers to be sorted.\n\n  Returns:\n    A new list with the numbers sorted in ascending order.\n  \"\"\"\n  sorted_list = list_to_sort.copy()\n  n = len(sorted_list)\n\n  # Iterate through the list starting from the second element\n  for i in range(1, n):\n    # Store the current element\n    key = sorted_list[i]\n    # Iterate backwards through the sorted portion\n    j = i - 1\n    while j >= 0 and key < sorted_list[j]:\n      # Shift elements to the right\n      sorted_list[j + 1] = sorted_list[j]\n      j -= 1\n    # Insert the key at the correct position\n    sorted_list[j + 1] = key\n\n  return sorted_list\n\n# Example usage\nmy_list = [1, 9, 5, 2, 1, 8, 6, 6, 3, 4, 10, 7]\nsorted_list = insertion_sort(my_list)\nprint(sorted_list)  # Output: [1, 1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10]\n```\n\n**Time Complexity of Insertion Sort:**\n\nInsertion sort has a time complexity of **O(n^2)** in the worst case, but it can be **O(n)** in the best case (when the list is already sorted).\n\n**Why Insertion Sort is Faster:**\n\n* **Adaptive:** Insertion sort is more efficient than bubble sort when the input list is partially sorted or nearly sorted.  It adapts to the input data and performs better than bubble sort in such cases.\n* **In-place sorting:** Both algorithms modify the original list directly, so they use minimal additional space.\n\n**Explanation:**\n\n* Insertion sort iterates through the list, building a sorted sublist one element at a time.\n* For each element, it finds the correct position in the sorted sublist and inserts it there. \n* In the best case, if the list is already sorted, it only performs 'n' operations (O(n)).\n* However, in the worst case, it still has to shift elements repeatedly, resulting in O(n^2) operations.\n\nIn general, insertion sort is a good choice when the input list is expected to be mostly sorted or when the size of the list is small. For larger lists with no specific ordering, other sorting algorithms like merge sort or quicksort are more efficient.\n",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)
