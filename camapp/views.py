from django.views.generic.base import TemplateView
from camapp.models import Empresa, Periodo, Viajes, Empleado
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.http.response import HttpResponseRedirect, HttpResponse
from datetime import date

class Home(TemplateView):
    template_name="home.html"
    
    def get_context_data(self,**kwargs):
        context=super(Home, self).get_context_data(**kwargs)
        context["empresas"]=Empresa.objects.all().order_by("nombre")
        return context

class EmpresaUpdate(UpdateView):
    template_name = "empresas/empresa_form.html"
    model = Empresa
    success_url = reverse_lazy("home")
    
class EmpresaCreate(CreateView):
    template_name="empresas/empresa_form.html"
    model = Empresa
    success_url = reverse_lazy("home")

class EmpleadosList(TemplateView):
    template_name = "empleados/list.html"
    
    def get_context_data(self, **kwargs):
        context=super(EmpleadosList, self).get_context_data(**kwargs)
        context["empresa"]=self.kwargs["empresa"]
        context["empleados"]= Empleado.objects.filter(empresa=self.kwargs["empresa"])
        return context

class EmpleadoUpdate(UpdateView):
    template_name = "empleados/empleado_form.html"
    model = Empleado
    
    def form_valid(self, form):
        self.object = form.save(commit=True)
        empresa = Empresa.objects.get(id=self.object.empresa.id)
        return HttpResponseRedirect(reverse_lazy("listaEmpleados", kwargs={'empresa':empresa.id}))
    
class EmpleadoCreate(CreateView):
    template_name="empleados/empleado_form.html"
    model = Empleado
    
    #def get_success_url(self):
    #    return HttpResponseRedirect(reverse_lazy("listaEmpleados", kwargs=(('empresa', self.kwargs["empresa"]))))
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        empresa = Empresa.objects.get(id=self.kwargs["empresa"])
        self.object.empresa = empresa
        self.object.save()
        return HttpResponseRedirect(reverse_lazy("listaEmpleados", kwargs={'empresa':self.kwargs["empresa"]}))

            
class PeriodoList(TemplateView):
    template_name = "periodos/list.html"
    
    def get_context_data(self, **kwargs):
        context=super(PeriodoList, self).get_context_data(**kwargs)
        context["chofer"]=Empleado.objects.get(id=self.kwargs["empleado"])
        context["periodos"]= Periodo.objects.filter(chofer=self.kwargs["empleado"])
        context["chofer_id"]=self.kwargs["empleado"]
        return context

class PeriodoCreate(CreateView):
    template_name = "periodos/periodo_form.html"
    model = Periodo
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        chofer = Empleado.objects.get(id=self.kwargs["empleado"])
        self.object.chofer = chofer
        self.object.save()
        return HttpResponseRedirect(reverse_lazy("listaPeriodos", kwargs={'empleado':self.kwargs["empleado"]}))
    
class ViajesList(TemplateView):
    template_name = "viajes/list.html"
    
    def get_context_data(self, **kwargs):
        context=super(ViajesList, self).get_context_data(**kwargs)
        context["chofer"]=Periodo.objects.get(id=self.kwargs["periodo"]).chofer
        context["periodo"]= Periodo.objects.get(id=self.kwargs["periodo"])
        context["viajes"]= Viajes.objects.filter(periodo=context["periodo"])
        return context
    
class ViajeCreate(CreateView):
    template_name = "viajes/viaje_form.html"
    model = Viajes
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        periodo = Periodo.objects.get(id=self.kwargs["periodo"])
        self.object.periodo = periodo
        self.object.save()
        return HttpResponseRedirect(reverse_lazy("listaViajes", kwargs={'periodo':self.kwargs["periodo"]}))
    
class ViajeUpdate(UpdateView):
    template_name = "viajes/viaje_form.html"
    model = Viajes
    
    def form_valid(self, form):
        self.object = form.save(commit=True)
        periodo = Periodo.objects.get(id=self.object.periodo.id)
        return HttpResponseRedirect(reverse_lazy("listaViajes", kwargs={'periodo':periodo.id}))
    
class ViajeDelete(DeleteView):
    template_name = "viajes/delete_confirm.html"
    model = Viajes
    
    def get_success_url(self):
        periodo = Periodo.objects.get(id=self.object.periodo.id)
        return reverse_lazy("listaViajes", kwargs={'periodo':periodo.id})
    
def exportarViajes(request, periodo):
    viajes = Viajes.objects.filter(periodo=periodo)
    bloque=""
    for viaje in viajes:
        bloque+=viaje.periodo.chofer.cuit.replace("-","")
        bloque+="|"
        bloque+=str(viaje.periodo.ano)
        bloque+="|"
        bloque+=str(viaje.periodo.mes)
        bloque+="|"
        bloque+=date.strftime(viaje.fecha_salida,"%d/%m/%Y")
        bloque+="|"
        bloque+="0"
        bloque+="|"
        bloque+=date.strftime(viaje.fecha_llegada,"%d/%m/%Y")
        bloque+="|"
        bloque+="0"
        bloque+="|"
        bloque+=str(viaje.kms_normales_recorridos)
        bloque+="|"
        bloque+=str(viaje.kms_extraordinarios_feriados)
        bloque+="|"
        bloque+=str(viaje.kms_extraordinarios_1_2)
        bloque+="|"
        bloque+=str(viaje.kms_extraordinarios_1_4)
        bloque+="|"
        bloque+=str(viaje.descargas)
        bloque+="|"
        bloque+="0"
        bloque+="|"
        bloque+=str(viaje.cruce_frontera)
        bloque+="|"
        bloque+=viaje.provincia_salida
        bloque+="|"
        bloque+=viaje.localidad_salida
        bloque+="|"
        bloque+=viaje.provincia_llegada
        bloque+="|"
        bloque+=viaje.localidad_llegada
        bloque+="|"
        bloque+=viaje.descanso
        bloque+="\n"
    return HttpResponse(bloque, content_type="text/plain")
    
    
    