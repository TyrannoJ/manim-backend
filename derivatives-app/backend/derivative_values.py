

from manim import *
import sympy as sp
import numpy as np
final_coefficients=[]
final_powers=[]
null_points=[]
extreme_points=[]
turning_points=[]

zeros_x_coords=[[],[],[]]

def create_functions(coefficients,powers):
    #calculate all important values
    for i in range(0,4):
        final_coefficients.append(coefficients.copy())
        final_powers.append(powers.copy())
        solutions=zero_points(coefficients,powers,i)
        if i !=3:
            if solutions:
                try:
                    for s in solutions:
                        
                        
                        
                        zeros_x_coords[i].append(s)
                        
                except:
                    print("weird zeros, don't worry")
                zeros_x_coords[i].sort()
            for i in range(0,len(powers)):
                coefficients[i],powers[i]=make_derivative(coefficients[i],powers[i])
    
    
def make_derivative(co,pow):
    co=round(co*pow,3)
    if pow >0:
        pow-=1
    return co,pow
def final_function(x,co,po):
    #calculate function value at point x
    y=0
    for i in range(0,len(po)):
        if po[i]>=0:
            y=y+co[i]*pow(x,po[i])
    return y
def zero_points(co,po,iteration):
    x = sp.Symbol('x')
    a=0
    for i in range(0,len(po)):
        if po[i]>=0:
            a=a+co[i]*x**po[i]
    
    points=sp.solveset(a,x,domain=sp.S.Reals)
    
    if co[0]==0 and po[0]<=0:
        points=sp.solveset(1,x,domain=sp.S.Reals)
    
    if iteration==1 and points:
        
        for p in points:
            extreme_points.append([p.evalf(3),final_function(p.evalf(3),final_coefficients[0],final_powers[0]).evalf(3)])
        extreme_points.sort(key=lambda item: item[0])
    if iteration==2:
        for p in extreme_points: #add type to extreme points
            value=""
            second_derivative_value=final_function(p[0],final_coefficients[2],final_powers[2])
            
            if second_derivative_value==0:
                value="TEP"
            if second_derivative_value>0:
                value="TIP"
            if second_derivative_value<0:
                value="HOP"
            p.append(value)
        if points:
            
            for p in points:
                
                turning_points.append([p.evalf(3),final_function(p.evalf(3),final_coefficients[0],final_powers[0]).evalf(3)])
        
            turning_points.sort(key=lambda item: item[0])
            

    if iteration==3:
        for p in turning_points: #add type to turning points
            value=""
            third_derivative_value=final_function(p[0],final_coefficients[3],final_powers[3])
            
            if third_derivative_value==0:
                left_value=final_function(p[0].evalf(3)-0.01,final_coefficients[2],final_powers[2])
                right_value=final_function(p[0].evalf(3)+0.01,final_coefficients[2],final_powers[2])
                
                value=""
                if left_value>0:
                    value=value+"L-"
                else:
                    value=value+"R-"

                if right_value>0:
                    value=value+"L"
                else:
                    value=value+"R"
            if third_derivative_value>0:
                value="R-L"
            if third_derivative_value<0:
                value="L-R"
            p.append(value)
        

    return(points)
def give_values(input):
    
    coefficients=[]
    powers=[]
    accepted=False

    #get User Input

    while accepted==False:
        accepted=True
        func=input
        #fu=func.split("+")
        fu=[""]
        #seperate equations
        element=0 
        for i,f in enumerate(func):
            if f != "+" and f != "-":

                fu[element]+=f
            else:
                if f=="+":
                    element+=1
                    fu.append("")
                elif f=="-":
                    
                    if i !=0:
                        element+=1
                        fu.append("")
                    fu[element]+="-"
                    
        
        for f in fu: #make equations to numbers
            has_x=False
            coefficient=""
            power=""
            for a in f:
                
                if 47<ord(a)<58 or a=="-" or a==".":
                    if has_x != True:
                        coefficient=coefficient+a
                    else:
                        power=power+a
                else:
                    has_x=True
            try:
                if coefficient=="":
                    coefficient="1"
                if coefficient=="-":
                    coefficient="-1"
                if has_x==False:
                    power=0
                if power=="":
                    power=1
                coefficients.append(float(coefficient))
                powers.append(int(power))
            except:
                accepted=False
                print("Invalid Input")
    create_functions(coefficients,powers)
    texts=[]       
    for i in range(0,3): # Draw Functions and Zeros (goes through all three functions)
        #plot functions and zeros
        coefficients=final_coefficients[i]
        powers=final_powers[i]        
        text=""
        for j,co in enumerate(zip(coefficients,powers)):
            if j==0 or str(co[0])[0]=="-" or co[1]<0:
                pass
            else:
                text+="+"
            if co[1]==0:
                text=text+rf"{co[0]}"
            elif co[1]==1:
                text=text+rf"{co[0]}*x"
            elif co[1]<0:
                text=text
            else:
                text=text+rf"{co[0]}*x^{co[1]}"
            texts.append(text)
    
    print(final_coefficients)
    print(final_powers)
    print(zeros_x_coords)
    print(extreme_points)
    print(turning_points)
    print(texts)
    #zeros von erster funktion besonders
    #hier funktionen zusammensetzen
         
        

give_values("3x3")

    
