import re
from typing import Optional


class OsciloScope: 
    Measured_data = []

    def __init__(self, corresponding_bookmark: (str)) -> None:
        self.corresponding_bookmark = corresponding_bookmark
        self._Average = None
        self._StandartDeviation = None
        self._Frequency = []
        OsciloScope.Measured_data.append(self)

    @property
    def Average(self):
        return self._Average 

    @Average.setter
    def Average(self, val):
        self._Average = val

    @Average.getter
    def Average(self):
        return self._Average
    
    @property
    def Frequency(self):
        return self._Frequency
    
    @Frequency.setter
    def Frequency(self, val):
        self._Frequency = val

    @property
    def StandartDeviation(self):
        return self._StandartDeviation 

    @StandartDeviation.setter
    def StandartDeviation(self, val):
        self._StandartDeviation = val

    @StandartDeviation.getter
    def StandartDeviation(self):
        return self._StandartDeviation
    


    @classmethod
    def Get_Obj_By_Bookmark(cls, bookmark: (str)) -> Optional[object]:
        for item in cls.Measured_data: 
            if item.corresponding_bookmark == bookmark:
                return item
        return None

    @classmethod
    def Create_and_Get_Average_and_STD_by_Bookmark(cls, bookmark: (str)) -> Optional[float]:
        import math
        for item in cls.Measured_data: 
            founded = item.corresponding_bookmark
            if founded == bookmark:
                inputList = item.Frequency
                if len(inputList) != 0:
                    
                    sum = 0
                    number_of_elements = len(inputList)
                    for number in inputList:
                        sum += number
                    average = sum / number_of_elements

                    deviation_sum = 0 

                    for number in inputList:
                        deviation_sum += math.pow((number - average), 2)

                    variance = deviation_sum / number_of_elements

                    St_Deviation = math.sqrt(variance)

                    item.Average = average
                    item.StandartDeviation =  St_Deviation
                    return [average,St_Deviation]
                else:
                    return [None, None]
        return  [None, None]

    @classmethod
    def Get_StDeviation_By_Bookmark(cls, bookmark: (str)) -> Optional[float]:
        for item in cls.Measured_data: 

            if item.corresponding_bookmark == bookmark:
                return item.StandartDeviation
        return None
    
    @classmethod
    def Get_Average_By_Bookmark(cls, bookmark: (str)) -> Optional[float]:
        for item in cls.Measured_data: 

            if item.corresponding_bookmark == bookmark:
                return item.Average
        return None
    @classmethod
    def Return_Cls_List(cls) -> list:
        return cls.Measured_data

    @classmethod
    def Show(cls):
        for item in cls.Measured_data: 
            print(f"{item.corresponding_bookmark} Average_Freq: {item.Average}, STD: {item.StandartDeviation}, Freq {item.Frequency} ")


with open(file= "test", mode='r') as file:
    for i,line in enumerate(file):
        if "added bookmark:" in line:
            pattern = r"Speed \[(\d+(?:\.\d+)?)\] rpm, Torque \[(\d+(?:\.\d+)?)\] Nm"
            result = re.findall(pattern=pattern, string=line)
            speed, torque = result[0]
            bookMark = f"Speed [{speed}] rpm, Torque [{torque}] Nm"
            OsciloScope(corresponding_bookmark=bookMark)
            breakLoop = False
            bookmarkLine = line
            j = 0
            while True: 
                if breakLoop:
                    break
                for j, line2 in enumerate(file):
                    if j > 50:
                        breakLoop = True
                        break
                    if "added bookmark:" in line2:
                        breakLoop = True
                        break
                    else:
                        match = re.findall(pattern=r"Frequency\((\d+)\)", string=line2)
                        if match:
                            pattern = r'\+\d+\.\d+E\+\d+'
                            freq= float(re.search(pattern, line2).group())
                            OsciloScope.Get_Obj_By_Bookmark(bookmark=bookMark).Frequency.append(freq)
           

print("#####################")    
print("OSCILOSCOPE DATA FROM TXT OSCILOSCOPE")
OsciloScope.Show()
     
                            
speeds= [100, 100.5, 250.00000005, 1399.99999995, 1600.00000005, 2250.0, 2749.9999999499996, 6000, 16142]
torques =  [30, 105, 135, 240, 270, 197.4]
print('\n')
print("#####################")    
print("Counting average and std from speed and torque values created in script")
for speed in speeds:
    for torq in torques:
        bookMark = (f"Speed [{speed}] rpm, Torque [{torq}] Nm")
        item  = OsciloScope.Create_and_Get_Average_and_STD_by_Bookmark(bookmark= bookMark)

        avg, std = item[0], item[1]
        print(f"For bookMark: {bookMark} is average: {avg}")
        