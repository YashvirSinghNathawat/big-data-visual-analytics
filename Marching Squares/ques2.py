#!/usr/bin/env python
# coding: utf-8

# In[327]:


from vtk import *
import math


# In[328]:


phong_shading = input("Do you want Phong Shading or not (Y/N): ")


# In[329]:


reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_3D.vti')
reader.Update()
data = reader.GetOutput()


# In[330]:


ctf = vtkColorTransferFunction()
ctf.AddRGBPoint(-4931.54, 0, 1, 1)
ctf.AddRGBPoint(-2508.95, 0, 0, 1)
ctf.AddRGBPoint(-1873.90, 0, 0, 0.5)
ctf.AddRGBPoint(-1027.16, 1, 0, 0)
ctf.AddRGBPoint(-298.031, 1, 0.4, 0)
ctf.AddRGBPoint(2594.97, 1, 1, 0)


# In[331]:


#Create a transfer function mapping scalar value to opacity
oTFun=vtkPiecewiseFunction()
oTFun.AddPoint(-4931.54, 1.0)
oTFun.AddPoint(101.815, 0.002)
oTFun.AddPoint(2594.97, 0.0)


# In[332]:


volumeProperty = vtkVolumeProperty()
volumeProperty.SetColor(ctf)
volumeProperty.SetScalarOpacity(oTFun)

if phong_shading=='Y' or phong_shading=='y':
    volumeProperty.ShadeOn()
else:
    volumeProperty.ShadeOff()
volumeProperty.SetInterpolationTypeToLinear()
volumeProperty.SetAmbient(0.5)
volumeProperty.SetDiffuse(0.5)
volumeProperty.SetSpecular(0.5)


# In[333]:


volumeMapper = vtkSmartVolumeMapper()
volumeMapper.SetInputData(data)


# In[334]:


volume = vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)


# In[335]:


outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outActor = vtkActor()
outActor.SetMapper(outline_mapper)
outActor.GetProperty().SetColor(0,0,0)
outActor.GetProperty().SetLineWidth(3)


# In[337]:


renWin = vtkRenderWindow()
ren1 = vtkRenderer()
ren1.SetBackground(255,255,255)
ren1.AddActor(outActor)
# ren1.AddActor(actor)
# ren1.AddLight(light)
ren1.AddViewProp(volume)
ren1.ResetCamera()
ren1.GetActiveCamera().SetClippingRange(1,100)
renWin.AddRenderer(ren1)
renWin.SetSize(1000,1000)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
renWin.Render()
iren.Start()


# In[ ]:




