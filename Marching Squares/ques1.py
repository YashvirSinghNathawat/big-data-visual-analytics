#!/usr/bin/env python
# coding: utf-8

# In[14]:


from vtk import *
import math


# In[15]:


reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()


# In[16]:


numCells = data.GetNumberOfCells()


# In[17]:


total_cells = vtkCellArray()
total_points = vtkPoints()


# In[18]:


C = int(input("Enter the contour value C = "))


# In[19]:


def checkCellType(cord1,cord2,cord3,cord4,C):
    cnt = 0
    if cord1>C:
        cnt+=1
    if cord2>C:
        cnt+=1
    if cord3>C:
        cnt+=1
    if cord4>C:
        cnt+=1
    return cnt


# In[20]:


def interpolation(cord1,cord2,pres1,pres2,C):
    if pres1<pres2:
        if C < pres1 or C>pres2:
            return ()
    elif pres2<pres1:
        if C<pres2 or C>pres1:
            return ()
    if cord1[0]==cord2[0]:
        return (cord1[0],(pres1-C)/(pres1-pres2)*(cord2[1]-cord1[1]) + cord1[1],cord1[2])
    else:
        return ((pres1-C)/(pres1-pres2)*(cord2[0]-cord1[0]) + cord1[0],cord1[1],cord1[2])


# In[21]:


cord1 = [0,0,0]
cord2 = [1,0,0]
cord4 = [1,1,0]


# In[22]:


for i in range(numCells):
    cell = data.GetCell(i)
    pid1 = cell.GetPointId(0)
    pid2 = cell.GetPointId(1)
    pid3 = cell.GetPointId(3)
    pid4 = cell.GetPointId(2)

    dataArr = data.GetPointData().GetArray('Pressure')
    val1 = dataArr.GetTuple1(pid1)
    val2 = dataArr.GetTuple1(pid2)
    val3 = dataArr.GetTuple1(pid3)
    val4 = dataArr.GetTuple1(pid4)
    pressure_values = [val1,val2,val3,val4]


    cord1 = data.GetPoint(pid1)
    cord2 = data.GetPoint(pid2)
    cord3 = data.GetPoint(pid3)
    cord4 = data.GetPoint(pid4)
    cord_values = [cord1,cord2,cord3,cord4]

    type_1 = val1>C
    type_2 = val2>C
    type_3 = val3>C
    type_4 = val4>C
    type_values = [type_1,type_2,type_3,type_4]

    black_count = checkCellType(val1,val2,val3,val4,C)
    
    if black_count==4 or black_count==0:
        continue

    elif black_count==1 or black_count==3:
        cand = -1
        
        for j in range(4):
            if type_values[(j-1+4)%4]!=type_values[j] and type_values[(j+1)%4]!=type_values[j]:
                cand = j

        point_1 = interpolation(cord_values[(cand-1+4)%4],cord_values[cand],pressure_values[(cand-1+4)%4],pressure_values[cand],C)
        point_2 = interpolation(cord_values[(cand+1)%4],cord_values[cand],pressure_values[(cand+1)%4],pressure_values[cand],C)
        
        
        if(point_1==() or point_2==()):
            continue

        total_points.InsertNextPoint(point_1)
        total_points.InsertNextPoint(point_2)


        polyLine = vtkPolyLine()
        polyLine.GetPointIds().SetNumberOfIds(2)    
        polyLine.GetPointIds().SetId(0,  total_points.GetNumberOfPoints() - 2)
        polyLine.GetPointIds().SetId(1,  total_points.GetNumberOfPoints() - 1)

        total_cells.InsertNextCell(polyLine)

    else:
        type_1 = val1>C
        type_2 = val2>C
        type_3 = val3>C
        type_4 = val4>C
        if type_1!=type_2 and type_1!=type_4:
            point_1 = ()
            point_2 = ()
            point_1 = interpolation(cord1,cord2,val1,val2,C)
            point_2 = interpolation(cord2,cord3,val2,val3,C)
            
            if point_1 == () or point_2 == ():
                continue

        else:
            point_1 = ()
            point_2 = ()
            if type_1==type_2:
                point_1 = interpolation(cord1,cord4,val1,val4,C)
                point_2 = interpolation(cord2,cord3,val2,val3,C)
            else:
                point_1 = interpolation(cord1,cord2,val1,val2,C)
                point_2 = interpolation(cord3,cord4,val3,val4,C)
            
            if point_1 == () or point_2 == ():
                continue
        total_points.InsertNextPoint(point_1)
        total_points.InsertNextPoint(point_2)

        # print(point_1,point_2)
        polyLine = vtkPolyLine()
        polyLine.GetPointIds().SetNumberOfIds(2)    
        polyLine.GetPointIds().SetId(0,  total_points.GetNumberOfPoints() - 2)
        polyLine.GetPointIds().SetId(1,  total_points.GetNumberOfPoints() - 1)

        total_cells.InsertNextCell(polyLine)
        

    


# In[23]:


pdata = vtkPolyData()

pdata.SetPoints(total_points)
pdata.SetLines(total_cells)
# pdata.GetPointData().AddArray(dataArray)


# In[24]:


### Store the polydata into a vtkpolydata file with extension .vtp
####################################################################
writer = vtkXMLPolyDataWriter()
writer.SetInputData(pdata)
writer.SetFileName('ques_1.vtp')
writer.Write()

