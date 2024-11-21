
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

        # example list of members
        self._members = []

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)


    def create_member(self, first_name, age, lucky_numbers, id=None):
        return {
            "id": id if id else self._generateId(),
            "first_name": first_name,
            "last_name": self.last_name,
            "age": age,
            "lucky_numbers": lucky_numbers
        }    

    def add_member(self, member):
    
        required_keys = ["first_name", "age", "lucky_numbers"]
        for key in required_keys:
            if key not in member:
                raise ValueError(f"'{key}' is required in the member data")

        if not isinstance(member["first_name"], str):
            raise ValueError("'first_name' must be a string")
        if not isinstance(member["age"], int) or member["age"] <= 0:
            raise ValueError("'age' must be an integer greater than 0")
        if not isinstance(member["lucky_numbers"], list) or not all(isinstance(num, int) for num in member["lucky_numbers"]):
            raise ValueError("'lucky_numbers' must be a list of integers")

        if "id" not in member:
            member["id"] = self._generateId()
        
        if "last_name" not in member:
            member["last_name"] = self.last_name
        
        self._members.append(member)


    def delete_member(self, id):
        # fill this method and update the return
        self._members = [member for member in self._members if member["id"] != id]


    def get_member(self, id):
        # fill this method and update the return
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
