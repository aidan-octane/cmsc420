# BST Variation 3

from __future__ import annotations
from typing import List
import json

verbose = False

i = 0

# The class for a particular node in the tree.
# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  age        : int       = None,
                  rownumbers : List[int] = [],
                  leftchild  : Node      = None,
                  rightchild : Node      = None):
        self.age        = age
        self.rownumbers = rownumbers
        self.leftchild  = leftchild
        self.rightchild = rightchild

# The class for a database.
# DO NOT MODIFY!
class DB():
    def __init__(self,
                 rows : List[List] = [],
                 root : Node       = None):
        self.rows = rows
        self.root = root

    # These dump_ methods are done for you.
    # DO NOT MODIFY!
    # Dump the rows of the database.
    def dump_rows(self) -> str:
        return('\n'.join([f'{i},{l[0]},{l[1]}' for i,l in enumerate(self.rows)]))
    # Dump the index of the database.
    def dump_index(self) -> str:
        def _to_dict(node) -> dict:
            return {
                "age"        : node.age,
                "rownumbers" : node.rownumbers,
                "leftchild"  : (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "rightchild" : (_to_dict(node.rightchild) if node.rightchild is not None else None)
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)
    
    def append_to_index(self, node : Node, age : int, j : int):
        if not node:
            self.root = Node(age, [j], None, None)
        elif (age < node.age and node.leftchild == None) or (age > node.age and node.rightchild == None):
            # If not in DB
            inserted_node = Node(age, [j], None, None)
            if age < node.age:
                # Add as left child
                node.leftchild = inserted_node
            else:
                # Add as right child
                node.rightchild = inserted_node
        elif age < node.age:
            self.append_to_index(node.leftchild, age, j)
        elif age > node.age:
            self.append_to_index(node.rightchild, age, j)
        else:
            node.rownumbers.append(j)

        
    def print_tree(self, root : Node):
        if root:
            print("Node " + str(root.age) + " - left child " + str(root.leftchild if not root.leftchild else root.leftchild.age) + ", right child " + str(root.rightchild if not root.rightchild else root.rightchild.age))
            self.print_tree(root.leftchild)
            self.print_tree(root.rightchild)
    # Holds current row number
    # Insert a row into the database and into the index.
    def insert(self,name: str, age: int):
        global i 
        # print("i: " + str(i))
        # Adds the entry into the database
        self.rows.append([name, age])
        # Recursively finds the 'age' node in the database and adds this index
        self.append_to_index(self.root,age,i)
        i = i+1
        # print("Added " + str(self.rows[i-1]) + " to index " + str(i-1))

    def search_for_age(self, node : Node, target_age : int) -> Node:
        if node.age == target_age:
            return node
        elif node.age > target_age:
            return self.search_for_age(node.leftchild, target_age)
        elif node.age < target_age:
            return self.search_for_age(node.rightchild, target_age)
        else:
            return None

    def index_one_over(self, node : Node, target_row_num : int):
        # Sorts through every node in the tree, and for each index that has any row numbers higher
        # than row_num, shift over by one (to match deletion)
        # print("Node row numbers before: " + str(node.rownumbers))
        i = 0
        for row_num in node.rownumbers:
            if row_num > target_row_num:
                node.rownumbers[i] = row_num - 1
            # elif row_num == target_row_num:
                # print("There is a Large Problem and you should DROP OUT!!")
            i = i+1
        # print("Node row numbers after: " + str(node.rownumbers))
        if node.leftchild: 
            self.index_one_over(node.leftchild, target_row_num)
        if node.rightchild:
            # self.print_tree(self.root)
            self.index_one_over(node.rightchild, target_row_num)



    # Deletes target node from BST
    def delete_node(self, root : Node, age : int):
        if root == None:
            return root
        if age < root.age:
            root.leftchild = self.delete_node(root.leftchild, age)
        elif age > root.age:
            root.rightchild = self.delete_node(root.rightchild, age)
        else:
            if root.leftchild is None:
                return root.rightchild  
            elif root.rightchild is None:
                return root.leftchild  
            else:
                successor = root.rightchild
                while successor.leftchild:
                    successor = successor.leftchild
                root.age = successor.age
                root.rownumbers = successor.rownumbers  
                root.rightchild = self.delete_node(root.rightchild, successor.age)
        return root


    # Delete a row from the database and from the index.
    # For the index since it's a BST use the inorder successor when a replacement is needed.
    def delete(self,name:str):
        # self.print_tree(self.root)
        # print("")
        global i
        i = i-1
        for j in range(len(self.rows) - 1, -1, -1):  
            # Find name in rows list
            if self.rows[j] and str(self.rows[j][0]) == name: #Potential error - two identical names
                age_of_popped_row = self.rows[j][1]
                # Pops from array (should shift everything over)
                # print("Pre-pop: " + str(self.rows))
                self.rows.pop(j)
                # print("Post-pop: " +str(self.rows))
                # Searches for the row number that we just popped from the database
                # print("calling search for age on root " + str(self.root.age) + " and row " + str(age_of_popped_row))
                # self.print_tree(self.root)
                node_with_row_num = self.search_for_age(self.root, age_of_popped_row)
                # print("Found node with row num to be " + str(node_with_row_num.age) + ", " + str(node_with_row_num.rownumbers))
                # Removes that row number from the proper age node's index
                k = 0
                for rownumber in node_with_row_num.rownumbers:
                    # print("Searching for j: " + str(j) + " in " + str(node_with_row_num.rownumbers))
                    if rownumber == j:
                        # print("Pre-pop k: " + str(node_with_row_num.rownumbers))
                        node_with_row_num.rownumbers.pop(k)
                        # print("Post-pop k: " + str(node_with_row_num.rownumbers))
                        break
                    k = k+1

                # Deletes node if necessary
                if not node_with_row_num.rownumbers:
                    self.root = self.delete_node(self.root, node_with_row_num.age)
                # Fixes row numbers in all other nodes, since all are shifted by one. O(n^2) and i Dont care
                # print("Calling index one over")
                # self.print_tree(self.root)
    
                self.index_one_over(self.root, j)

                

    # Use the index to find a list of people whose age is specified.
    # This should return a list of the form:
    # [d,n1,n2,...]
    # Where d is the depth of the appropriate node in the index (BST)
    # and n1,n2,... are the people.
    def find_people(self,age:int):
        # self.print_tree(self.root)
        d = 0
        l = []
        # Find proper node and count levels
        curr_node = self.root
        while curr_node and curr_node.age != age:
            if curr_node.age < age:
                curr_node = curr_node.rightchild
            else:
                curr_node = curr_node.leftchild
            d = d+1
        # Populate 'l' with people from the database with that age
        for rownumber in curr_node.rownumbers:
            l.append(self.rows[rownumber][0]) 
        # Return the result.
        return [d] + l 