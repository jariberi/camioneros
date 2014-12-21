from django.conf.urls import patterns, include, url
from camapp import views

empresasPattern = patterns('',
    url(r'nuevo$', views.EmpresaCreate.as_view(), name='agregarEmpresa'),
    url(r'editar/(?P<pk>\d+)$', views.EmpresaUpdate.as_view(), name='editarEmpresa'),
    )

empleadosPattern = patterns('',
    url(r'listar/(?P<empresa>\d+)$', views.EmpleadosList.as_view(), name='listaEmpleados'),
    url(r'(?P<empresa>\d+)/nuevo$', views.EmpleadoCreate.as_view(), name='agregarEmpleado'),
    url(r'editar/(?P<pk>\d+)$', views.EmpleadoUpdate.as_view(), name='editarEmpleado'),
    )

periodosPattern = patterns('',
    url(r'listar/(?P<empleado>\d+)$', views.PeriodoList.as_view(), name='listaPeriodos'),
    url(r'(?P<empleado>\d+)/nuevo$', views.PeriodoCreate.as_view(), name='agregarPeriodo'),
    )

viajesPattern = patterns('',
    url(r'listar/(?P<periodo>\d+)$', views.ViajesList.as_view(), name='listaViajes'),
    url(r'exportar/(?P<periodo>\d+)$', views.exportarViajes, name='exportarViajes'),
    url(r'(?P<periodo>\d+)/nuevo$', views.ViajeCreate.as_view(), name='agregarViaje'),
    url(r'editar/(?P<pk>\d+)$', views.ViajeUpdate.as_view(), name='editarViaje'),
    url(r'borrar/(?P<pk>\d+)$', views.ViajeDelete.as_view(), name='borrarViaje'),
    )


urlpatterns = patterns('',
    url(r'^$',views.Home.as_view(), name='home'),
    url(r'^empresas/', include(empresasPattern)),
    url(r'^choferes/', include(empleadosPattern)),
    url(r'^periodos/', include(periodosPattern)),
    url(r'^viajes/', include(viajesPattern)),
    )
