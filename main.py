import time

from isaacsim import SimulationApp
# import isaacsim.core.utils.prims as prim_utils

simulation_app = SimulationApp({"headless": False})

import omni.usd
stage = omni.usd.get_context().get_stage()

from pxr import UsdGeom, Gf, UsdLux, Sdf, UsdShade

def define_environment():
    # Add a light
    dome_light = UsdLux.DomeLight.Define(stage, Sdf.Path("/World/DomeLight"))
    dome_light.CreateIntensityAttr(5000.0)          # Set the dome light intensity
    dome_light.CreateColorAttr((1.0, 1.0, 1.0))     # White light


def define_materials():
    mat_infos = [
       ((1.0, 0.0, 0.0), "Red"),
       ((0.0, 1.0, 0.0), "Green"),
       ((0.0, 0.0, 1.0), "Blue"),
       ((1.0, 0.0, 1.0), "Magenta"),
       ((0.0, 1.0, 1.0), "Cyan"),
       ((1.0, 1.0, 0.0), "Yellow"),
    ]
    mat_infos_d = {
       "Red":{"dclr":(1.0, 0.0, 0.0), "ruff": 0.2, "metal":0.0,"opaque":1.0},
       "Green":{"dclr":(0.0, 1.0, 0.0), "ruff": 0.2, "metal":0.0,"opaque":0.5},
       "Blue":{"dclr":(0.0, 0.0, 1.0), "ruff": 0.2, "metal":0.0,"opaque":0.1},
    }
    mats = []
    ln_mat = len(mat_infos_d)
    for k in mat_infos_d:
        mspec = mat_infos_d[ k]
        color = mspec["dclr"]
        ruff = mspec["ruff"]
        metal = mspec["metal"]
        opaque = mspec["opaque"]
        mat_path = Sdf.Path(f"/World/Looks/Mat{k}")
        material = UsdShade.Material.Define(stage, mat_path)
        shader = UsdShade.Shader.Define(stage, mat_path.AppendPath("Shader"))
        shader.CreateIdAttr("UsdPreviewSurface")
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(color)
        shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(ruff)
        shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(metal)
        shader.CreateInput("opacity", Sdf.ValueTypeNames.Float).Set(opaque)        
        material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
        mats.append(material)
    return mats

def define_cubes(mats):

    lnmat = len(mats)
    for i in range(10):
    
        path = Sdf.Path(f"/World/Cube_{i}")
        print(f"Defining {path}")
           
        cube = UsdGeom.Cube.Define(stage, path)
        cube.AddTranslateOp().Set(Gf.Vec3f(i * 2.2, 0, 0))
        mat = mats[i % lnmat]
   
        UsdShade.MaterialBindingAPI(cube).Bind(mat)
        
def define_cube_of_cubes(mats,nx,ny,nz, dx, dy, dz):

    lnmat = len(mats)
    i = 0
    n = nx*ny*nz
    for x in range(nx):
        for y in range(ny):
            for z in range(nz):
    
                path = Sdf.Path(f"/World/Cube_{x}_{y}_{z}")
                
                if i % 200 == 0:
                    print(f"Defining {path}  {i} of {n}")
           
                cube = UsdGeom.Cube.Define(stage, path)
                cube.AddTranslateOp().Set(Gf.Vec3f( x*dx*2.2, y*dy*2.2,  z*dz*2.2 ))
                cube.AddScaleOp().Set(Gf.Vec3f( dx, dy,  dz ))
                mat = mats[i % lnmat]
   
                UsdShade.MaterialBindingAPI(cube).Bind(mat)
                i += 1

def define_stuff():
    define_environment()
    mats = define_materials()
    fak = 1
    sz = 0.1 / fak
    define_cube_of_cubes(mats,fak*20,fak*10,fak*10, sz, sz, sz)


def main():
    start = time.time()
    define_stuff()
    elap = time.time() - start
    print(f"Definition took {elap:.1f} secs")
    
    while simulation_app.is_running():
            # perform step
        simulation_app.update()        
        # sim.step()
    
    simulation_app.close()


main()