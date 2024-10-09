class ScheduleItem:
    def __init__(self, nombre: str, grupo: str = None, cuatrimestre: int = None, 
                 calif_cuatrimestre: int = None, calif_holgura: int = None, 
                 calif_seriacion: int = None, lunes: list = None, 
                 martes: list = None, miercoles: list = None, 
                 jueves: list = None, viernes: list = None, id: int = None):    
        self.id = id
        self.nombre = nombre
        self.grupo = grupo
        self.cuatrimestre = cuatrimestre
        self.calif_cuatrimestre = calif_cuatrimestre
        self.calif_holgura = calif_holgura
        self.calif_seriacion = calif_seriacion
        self.lunes = lunes
        self.martes = martes
        self.miercoles = miercoles
        self.jueves = jueves
        self.viernes = viernes

    def __repr__(self):
        return f"<ScheduleItem {self.nombre}>"