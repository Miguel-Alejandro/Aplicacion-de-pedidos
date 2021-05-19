from django.shortcuts import render, redirect

#import necesario para hacer funcionar el buscador
from django.db.models import Q

#importa lo necesario para que funcione el metodo GET y POST
from rest_framework.decorators import api_view
from rest_framework import generics

from .models import hoyRX, item
from .serializer import hoyRXSerializer, itemSerializer
from .forms import GenerarPedidosForm,registroUsuarioForm

#importa lo necesario para que funcione la autenticacion
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



class hoyRxList(generics.ListCreateAPIView):
    queryset = hoyRX.objects.all()
    serializer_class = hoyRXSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)



#LOGIN
class Login(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('api:hoyRx_List')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())

        else:
            return super(Login,self).dispatch(request,*args,*kwargs)

    def form_valid(self,form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)

        if token:
            login(self.request, form.get_user())
            return super(Login, self).form_valid(form)





#LOGOUT

class Logout(APIView):
    def get(self, request, format = None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status = status.HTTP_200_OK)




#funcion de get y post para el modelo item
@api_view(['GET', 'POST'])
def items(request):

    if request.method == 'GET':
        Item = item.objects.all()
        serializer = itemSerializer(Item, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = itemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





#funcion para mandar informacion al modelo hoyRX
@api_view(['POST'])
def hoyRxPost(request):

    request.method == 'POST'
    serializer = hoyRXSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#templates

def inicio(request):
    #funcion del buscador en la vista pedidos
    queryset = request.GET.get('buscar')
    Item = item.objects.all()

    if queryset:
        Item = item.objects.filter(
            Q(date__icontains = queryset)
        )

        return render(request, 'index.html', {'item':Item})




    Item = item.objects.all()

    contexto = {
        'item':Item,
    }

    return render(request, 'index.html', contexto)


def crearPedido(request):

    #funcion del formulario
    if request.method == 'GET':
    
        Item = item.objects.all()
        hoyrx = hoyRX.objects.all()
        contexto = {
            'item':Item,
            'hoyrx':hoyrx
        }


        #funcion del buscador en generar pedidos
        queryset = request.GET.get('buscar')
        hoyrx = hoyRX.objects.all()

        if queryset:
            hoyrx = hoyRX.objects.filter(
                Q(name__icontains = queryset) |
                Q(email__icontains = queryset) |
                Q(last_name__icontains = queryset)
            ).distinct()

            return render(request,'crearPedido.html', {'hoyrx':hoyrx})



    else:
        form = GenerarPedidosForm(request.POST)
        contexto = {
            'form': form,
        }

        if form.is_valid():
            form.save()
            return redirect('index')


    return render(request, 'crearPedido.html', contexto)




def regUsuario(request):
   
    if request.method == 'GET':
        Hoyrx = hoyRX.objects.all()
        contexto = {
            'hoyrx':Hoyrx
        }


    else:
        form = registroUsuarioForm(request.POST)
        contexto = {
            'form':form
        }

        print(form)

        if form.is_valid():
            form.save()
            return redirect('index')
        


    return render(request, 'regUsuario.html', contexto)

