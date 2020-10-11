#This class will elaborate quizes about states and save them to a designated path.
#Maurilio
import random, re

class RandomQuiz:
    _states_dictionary = {"Aguascalientes" : "Aguascalientes", "Baja California" : "Mexicali",
                          "Baja California Sur" : "La Paz", "Campeche" : "Campeche", "Coahuila" : "Saltillo",
                          "Colima" : "Colima",  "Chiapas" : "Tuxtla Gutiérrez", "Chihuahua" : "Chihuahua",
                          "Durango" : "Durango", "Guanajuato" : "Guanajuato", "Guerrero" : "Chilpancingo",
                          "Hidalgo" : "Pachuca", "Jalisco" : "Guadalajara", "México" : "Toluca",
                          "Michoacán" : "Morelia", "Morelos" : "Cuernavaca", "Nayarit" : "Tepic",
                          "Nuevo León" : "Monterrey", "Oaxaca" : "Oaxaca", "Puebla" : "Puebla",
                          "Querétaro" : "Querétaro", "Quintana Roo" : "Chetumal", "San Luis Potosí" : "San Luis Potosí",
                          "Sinaloa" : "Culiacán", "Sonora": "Hermosillo", "Tabasco" : "Villahermosa",
                          "Tamaulipas" : "Ciudad Victoria", "Tlaxcala" : "Tlaxcala", "Veracruz" : "Xalapa",
                          "Yucatán" : "Mérida", "Zacatecas" : "Zacatecas"
                          }

    _alphabet = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z")

    def __init__(self):
        #self.generateQuestion()
        self.generateQuestions(10,8)
        path = ".\\tempfiles\\"
        self.generateExams(path,30,10,8)

    def getRandomState(self):
        states = list(self._states_dictionary.keys())
        return states[random.randint(0, len(states)-1)]

    def getRandomCapitals(self, state, num):
        capitals = list(self._states_dictionary.values())
        answers = []
        answers.append(self._states_dictionary.get(state))
        while len(answers) < num:
            capital = capitals[random.randint(0, len(capitals)-1)]
            if not self.exists(answers,capital):
                answers.append(capital)
        new_answers = []
        while len(answers)>0:
            new_answers.append(answers.pop(random.randint(0,len(answers)-1)))
        return new_answers

    def exists(self, list, value):
        for l in list:
            if l == value:
                return True
        return False

    def generateQuestion(self):
        state = self.getRandomState()
        string = "Which is the capital of "+state+"?\n"
        capitals = self.getRandomCapitals(state,5)
        for i in range(len(capitals)):
            string += self._alphabet[i]+") "+capitals[i] + "\n"
        string += "\n"
        print(string)

    def generateQuestions(self, numberquestions, numberanswers):
        states = []
        options = []
        strquestions = ""
        stranswers = ""
        i = 0
        while len(states) < numberquestions:
            state = self.getRandomState()
            if not self.exists(states,state):
                states.append(state)
                capitals = self.getRandomCapitals(state,numberanswers)
                options.append(capitals)
                strquestions += str(i+1) + ".- Which is the capital of " + state + "?\n"
                stranswers += str(i + 1) + ".- "
                for j in range(len(capitals)):
                    strquestions += self._alphabet[j]+") "+capitals[j]+"\n"
                    regexpattern = r".*"+self._states_dictionary.get(state)+r"$"
                    if re.search(regexpattern,capitals[j]) != None:
                        stranswers += self._alphabet[j]+") "+capitals[j]
                strquestions += "\n"
                stranswers += "\n"
                i += 1
        print(strquestions)
        print(stranswers)
        return strquestions, stranswers

    def generateExams(self,examspath, numberexams, numberquestions, numberanswers):
        examfilename = "EXAM"
        answersfilename = "ANSWERS"
        filextension = ".TXT"

        print("Generating exams...")

        for i in range(numberexams):
            strexam = "EXAM NO: "+str(i+1)
            strexam += "\n Student Name: _________________________________________________"
            strexam += "\n Date: _____/_____/_____"
            strexam += "\n Instructions: Please circle the correct answer for every question."
            strexam += "\n"
            questions, answers = self.generateQuestions(numberquestions,numberanswers)
            strexam += questions
            stranswers = "ANSWERS FOR EXAM NO: "+str(i+1) + "\n" + answers

            filename = examspath + examfilename + str(i+1) + filextension
            with open(filename,"w") as f:
                f.write(strexam)
                print("File exam: "+filename+" saved to disk")

            filename = examspath + answersfilename + str(i+1) + filextension
            with open(filename,"w") as f:
                f.write(stranswers)
                print("File answers: "+filename+" saved to disk")

            print("Finishing exam generation.")





