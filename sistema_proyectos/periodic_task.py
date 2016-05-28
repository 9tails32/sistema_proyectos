import threading
import time
from sprint.models import Sprint

#def verificar_sprints():
#    sprints = Sprint.objects.all()
#    for sprint in sprints:
#        print sprint.nombre

#def worker():
#    """funcion que realiza el trabajo en el thread"""
#   while(True):
#        verificar_sprints()
#        time.sleep(30)
#    return

#def iniciar_task():
#    t = threading.Thread(target=worker)
#    t.start()
