class CategoryClass():
    frompath = ""

    def getClassNames(self):
        classNames = []
        for key, value in self.frompath.items():
            classNames.append(key)
        return classNames

    def getAllObjectsOfTopology(self):
        classNames = []
        for key, value in self.frompath['topology'].items():
            if value.__class__.__name__ not in classNames:
                classNames.append(value.__class__.__name__)
        return classNames

    def getClassData(self):
        classData = ''
        for key, value in self.frompath['topology'].items():
            if value.__class__.__name__ in self.getAllObjectsOfTopology():
                if isinstance(value, list):
                    classData += value[0] + "\n llllll \n"
                else:
                    classData += value.__str__() + "\n llllll \n"
        return classData

    # search for data by class name and returns a String
    def getObjectbyClass(self, className):
        className = "class=" + className
        classData = ''
        for key, value in self.frompath['topology'].items():
            if className in value.__str__():
                classData += value.__str__() + "\n"
        return classData

    def getObjectbyID(self):
        # className="class="+className
        classData = ''
        classData = self.frompath['topology'].items()
        # for key, value in self.frompath['topology'].items():
        #     if className in value.__str__():
        #         classData+=value.__str__()+"\n"
        return classData
