import yaml

import random
import math

class Preferences:
    likescheese = True

class Data:
    GeneratorData = None
    Data = None

    placeholders = [
            "(づ￣ ³￣)づ",
            "( ˘ ³˘)♥",
            "(ง'̀-'́)ง",
            "{•̃_•̃}",
            "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
            "(っ˘ڡ˘ς)",
            "(งツ)ว",
            "ʕʘ̅͜ʘ̅ʔ",
            "\(ᵔᵕᵔ)/",
            "(._.)",
            "(っ•́｡•́)♪♬",
            "(•̀ᴗ•́)و ̑̑",
            "(ᵔᴥᵔ)",
            "◖ᵔᴥᵔ◗ ♪ ♫",
            "♪♪ ヽ(ˇ∀ˇ )ゞ",
            "ヽ(´▽`)/",
            "ʕ·͡ᴥ·ʔ",
            "ʕっ•ᴥ•ʔっ",
            "( ˘ ³˘)ノ°ﾟº❍｡",
            "(͡ ° ͜ʖ ͡ °)",
            "(｡◕‿‿◕｡)",
            "(ᕗ ͠° ਊ ͠° )ᕗ",
            "ᕕ(⌐■_■)ᕗ ♪♬",
            "(◕ᴥ◕ʋ)",
            "(҂◡_◡) ᕤ",
            "(ﾉ◕ヮ◕)ﾉ*:・ﾟ✧",
            "(ง •̀_•́)ง",
            "(✿◠‿◠)",
            "( つ◕ل͜◕)つ",
            "༼ つ ╹ ╹ ༽つ",
            "(*・‿・)ノ⌒*:･ﾟ✧",
            "(ﾉ☉ヮ⚆)ﾉ ⌒*:･ﾟ✧",
            "༼つಠ益ಠ༽つ ─=≡ΣO))",
            "٩( ๑╹ ꇴ╹)۶",
            "._.)/\(._.",
            "(づ｡◕‿‿◕｡)づ",
            "／人◕ ‿‿ ◕人＼"
        ]

    def GetPlaceholder():
        return Data.placeholders[random.randint(0, len(Data.placeholders))-1]

    # Load UserData
    def Load():
        with open("UserData.yaml") as stream:
            try:
                Data.GeneratorData = yaml.safe_load_all(stream)
                Data.Data = list(Data.GeneratorData)

                Data.GenerateData()
            except yaml.YAMLError as exc:
                print(exc)
                return None

    def GenerateData():
        # Get all possible keys
        Data.StoredKeys = []   # Columns
        Data.StoredValues = []   # Rows

        # Generate keys
        for row in range(len(Data.Data)):
            key = list(Data.Data[row].keys())

            for column in range(math.floor(len(key) / 2)):
                if key not in Data.StoredKeys:
                    Data.StoredKeys.append(key)

        Data.StoredKeys = sum(Data.StoredKeys, []) # Convert keys to 1 dimensional array

        # Generate values
        for column in range(len(Data.Data)):
            value = list(Data.Data[column].values())

            for row in range(math.floor(len(value) / 2)):
                Data.StoredValues.append(value)

    # Update UserData
    def Update(item, row, column):
        if item != None:
            # Set the data
            Data.Data[row][Data.StoredKeys[column]] = item.text()   
            
            with open("UserData.yaml", "w") as f:
                yaml.safe_dump_all(Data.Data, f)
    
    # Add a document
    def AddDoc():
        # Creates an empty document with all keys filled with an empty placeholder in UserData.yaml
        with open("UserData.yaml", "w") as f:
            dic = {}

            for v in Data.StoredKeys:
                dic[v] = Data.GetPlaceholder()
            
            Data.Data.append(dict(dic))
            yaml.safe_dump_all(Data.Data, f)

    # Delete a document
    def DelDoc(i):
        with open("UserData.yaml", "w") as f:
            del Data.Data[i]
            yaml.safe_dump_all(Data.Data, f)