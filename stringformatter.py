class StringUtilityFormatter:

    @staticmethod
    def getFirstName(full_name: str) -> str:
        first_name = []
        for char in full_name:
            if char != ' ':
                first_name.append(char)
            else:
                break
        return "".join(first_name)