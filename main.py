import time
import math

from isaacsim import SimulationApp
# import isaacsim.core.utils.prims as prim_utils

simulation_app = SimulationApp({"headless": False})

import omni.usd
stage = omni.usd.get_context().get_stage()

from pxr import UsdGeom, Gf, UsdLux, Sdf, UsdShade

def add_planes(mats):
    psz = 15
    thin_psize = 0.01*psz
    planeXY = UsdGeom.Cube.Define(stage, "/XY_plane")
    planeXY.AddTranslateOp().Set(Gf.Vec3f( 0, 0, 0 ))
    planeXY.AddScaleOp().Set(Gf.Vec3f( psz, psz,  thin_psize ))       
    UsdShade.MaterialBindingAPI(planeXY).Bind(mats["BlueTrans"])

    planeYZ = UsdGeom.Cube.Define(stage, "/YZ_plane")
    planeYZ.AddTranslateOp().Set(Gf.Vec3f( 0, 0, 0 ))
    planeYZ.AddScaleOp().Set(Gf.Vec3f( thin_psize, psz,  psz ))       
    UsdShade.MaterialBindingAPI(planeYZ).Bind(mats["RedTrans"])
    
    planeZX = UsdGeom.Cube.Define(stage, "/ZX_plane")
    planeZX.AddTranslateOp().Set(Gf.Vec3f( 0, 0, 0 ))
    planeZX.AddScaleOp().Set(Gf.Vec3f( psz, thin_psize,  psz ))       
    UsdShade.MaterialBindingAPI(planeZX).Bind(mats["GreenTrans"])

   

def add_vek(v1,v2):
    v3 = Gf.Vec3f( v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2] )
    return v3
    
def add_rods(mats):
    rodlen = 15
    rodmarkspace = 5   
    rod_thick = 0.05
    mark_sz = rod_thick*3
    mkclr = mats["Black"]
    
    rodclr = mats["Red"]
    rska = Gf.Vec3f( rodlen, rod_thick, rod_thick)
    mpos = Gf.Vec3f( -rodlen, 0, 0 )
    minc = Gf.Vec3f( rodmarkspace, 0, 0 )      
    rodname = "/rods/X_rod"
    
    mcur = -rodlen
    rod = UsdGeom.Cube.Define(stage, rodname)
    rod.AddScaleOp().Set(rska)       
    UsdShade.MaterialBindingAPI(rod).Bind(rodclr)
    mk = 1
    while mcur<=rodlen:
        if mcur!=0:
            markname = f"{rodname}_m{mk}"
            mk += 1
            mark = UsdGeom.Sphere.Define(stage, markname )
            mark.AddTranslateOp().Set(mpos)
            mark.AddScaleOp().Set(Gf.Vec3f( mark_sz, mark_sz,  mark_sz ))
            UsdShade.MaterialBindingAPI(mark).Bind(mkclr)
        mcur += rodmarkspace        
        mpos = add_vek( mpos, minc )


    rodclr = mats["Green"]
    rska = Gf.Vec3f( rod_thick, rodlen, rod_thick)
    mpos = Gf.Vec3f( 0, -rodlen, 0 )
    minc = Gf.Vec3f( 0, rodmarkspace, 0 )
    rodname = "/rods/Y_rod"
    
    mcur = -rodlen
    rod = UsdGeom.Cube.Define(stage, rodname)
    rod.AddScaleOp().Set(rska)       
    UsdShade.MaterialBindingAPI(rod).Bind(rodclr)
    mk = 1
    while mcur<=rodlen:
        if mcur!=0:
            markname = f"{rodname}_m{mk}"
            mk += 1
            mark = UsdGeom.Sphere.Define(stage, markname )
            mark.AddTranslateOp().Set(mpos)
            mark.AddScaleOp().Set(Gf.Vec3f( mark_sz, mark_sz,  mark_sz ))
            UsdShade.MaterialBindingAPI(mark).Bind(mkclr)
        mcur += rodmarkspace    
        mpos = add_vek( mpos, minc )


    rodclr = mats["Blue"]
    rska = Gf.Vec3f( rod_thick, rod_thick,  rodlen )
    mpos = Gf.Vec3f( 0, 0, -rodlen )
    minc = Gf.Vec3f( 0, 0, rodmarkspace )
    rodname = "/rods/Z_rod"
    
    mcur = -rodlen
    rod = UsdGeom.Cube.Define(stage, rodname)
    rod.AddScaleOp().Set(rska)       
    UsdShade.MaterialBindingAPI(rod).Bind(rodclr)
    mk = 1
    while mcur<=rodlen:
        if mcur!=0:            
            markname = f"{rodname}_m{mk}"
            mk += 1
            mark = UsdGeom.Sphere.Define(stage, markname )
            mark.AddTranslateOp().Set(mpos)
            mark.AddScaleOp().Set(Gf.Vec3f( mark_sz, mark_sz,  mark_sz ))
            UsdShade.MaterialBindingAPI(mark).Bind(mkclr)
        mcur += rodmarkspace
        mpos = add_vek( mpos, minc )


def define_environment(mats):

    # Z-up more common in Engineering and Medical, Y-up in Gaming and modelling
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z) 
    # Add a light
    dome_light = UsdLux.DomeLight.Define(stage, Sdf.Path("/World/DomeLight"))
    dome_light.CreateIntensityAttr(800.0)          # Set the dome light intensity
    dome_light.CreateColorAttr((1.0, 1.0, 1.0))     # White light
    
    sphere = UsdGeom.Sphere.Define(stage, "/World/Origin")    
    sphere.AddTranslateOp().Set(Gf.Vec3f( 0, 0, 0 ))
    sphere.AddScaleOp().Set(Gf.Vec3f( 1, 1,  1 ))    
    
    # add_planes(mats)
    add_rods(mats)
    



def define_materials():
    mat_infos = [
       ((1.0, 0.0, 0.0), "Red"),
       ((0.0, 1.0, 0.0), "Green"),
       ((0.0, 0.0, 1.0), "Blue"),
       ((1.0, 1.0, 0.0), "Magenta"),
       ((0.0, 1.0, 1.0), "Cyan"),
       ((1.0, 0.0, 1.0), "Yellow"),
    ]
    mat_infos_d = {
       "White":{"dclr":(1.1, 1.1, 1.1), "ruff": 0.2, "metal":0.0,"opaque":1.0},
       "Black":{"dclr":(0.0, 0.0, 0.0), "ruff": 0.2, "metal":0.0,"opaque":1.0},
       "Red":{"dclr":(1.1, 0.0, 0.0), "ruff": 0.2, "metal":0.0,"opaque":1.0},
       "Green":{"dclr":(0.0, 1.1, 0.0), "ruff": 0.2, "metal":0.0,"opaque":1.0},
       "Blue":{"dclr":(0.0, 0.0, 1.1), "ruff": 0.2, "metal":0.0,"opaque":1.0},
       "Magenta":{"dclr":(1.0, 0.0, 1.0), "ruff": 0.2, "metal":0.0,"opaque":1.0},
       "Cyan":{"dclr":(0.0, 1.0, 1.0), "ruff": 0.2, "metal":0.0,"opaque":1.0},
       "Yellow":{"dclr":(1.0, 1.0, 0.0), "ruff": 0.2, "metal":0.0,"opaque":1.0},
       "RedTrans":{"dclr":(1.1, 0.0, 0.0), "ruff": 0.2, "metal":0.0,"opaque":0.3},
       "GreenTrans":{"dclr":(0.0, 1.1, 0.0), "ruff": 0.2, "metal":0.0,"opaque":0.3},
       "BlueTrans":{"dclr":(0.0, 0.0, 1.1), "ruff": 0.2, "metal":0.0,"opaque":0.3},
       "Blood":{"dclr":(1.0, 0.0, 0.0), "ruff": 0.2, "metal":0.0,"opaque":0.2},
       "Vessel":{"dclr":(0.1, 0.1, 1.1), "ruff": 0.2, "metal":0.0,"opaque":0.9},
       "Stuff":{"dclr":(0.5, 0.5, 0.5), "ruff": 0.2, "metal":0.0,"opaque":0.2},
    }
    mats = {}
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
        mats[k] = material
    return mats
    
def filter_mats(mats,names):
    newmats = {}
    for k in names:
        if k in mats:
            newmats[k] = mats[k]
        else:
            print(f"Missing material {k}")
            keys_list = list(mats.keys())            
            print(f"Defined:{keys_list}")
    return newmats

def define_cubes(mats):

    lnmat = len(mats)
    for i in range(10):
    
        path = Sdf.Path(f"/World/Cube_{i}")
        print(f"Defining {path}")
           
        cube = UsdGeom.Cube.Define(stage, path)
        cube.AddTranslateOp().Set(Gf.Vec3f(i * 2.2, 0, 0))
        mat = mats[i % lnmat]
   
        UsdShade.MaterialBindingAPI(cube).Bind(mat)
        
def define_cube_of_cubes(mats, nx,ny,nz, need_len, irad, orad):
    mats_list = list(mats.values())
    lnmat = len(mats_list)
    n = nx*ny*nz
    cc_gap = 0.1
    cc_size = 2
    cc_inioff = cc_size/2 # cube centers are coordinate orgin centered 
    cc_dd = (cc_size + cc_gap)
    cc_tdx = (nx*cc_size + (nx-1)*cc_gap) 
    cc_tdy = (ny*cc_size + (ny-1)*cc_gap) 
    cc_tdz = (nz*cc_size + (nz-1)*cc_gap) 
    
    sz = need_len / cc_tdx
    
    inioff = sz*cc_inioff
    dd = sz*cc_dd
    tdx = sz*cc_tdx
    tdy = sz*cc_tdy
    tdz = sz*cc_tdz
    shiftx = tdx/2 - inioff
    shifty = tdy/2 - inioff
    shiftz = tdz/2 - inioff
    # shfitx = shifty = shiftz = 0
    print(f"Total cube_of_cube size x:{tdx:.2f} y:{tdy:.2f} z:{tdz:.2f}") 
    ic = 0
    ig = 0
    for ix in range(nx):
        x = ix*dd - shiftx
        for iy in range(ny):
            y = iy*dd - shifty
            for iz in range(nz):          
                z = iz*dd - shiftz
                distyz = math.sqrt(y*y + z*z)
                if distyz<irad:
                     imat = 0
                elif distyz<orad:
                     imat = 1
                else:
                     imat = 2  
                mat = mats_list[imat]   
                if imat<2:             
                    usdpath = Sdf.Path(f"/World/Coc/Cube_{ix}_{iy}_{iz}")                
                    if ic % 200 == 0:
                        print(f"Defining cube:{ic} {usdpath} - {ig} of {n}")
                    cube = UsdGeom.Cube.Define(stage, usdpath)
                    cube.AddTranslateOp().Set(Gf.Vec3f( x, y, z ))
                    cube.AddScaleOp().Set(Gf.Vec3f( sz, sz,  sz ))
                    UsdShade.MaterialBindingAPI(cube).Bind(mat)
                    ic += 1
                ig += 1

def define_stuff():

    pop_adj_fak = 6
    nx = round(pop_adj_fak*20)
    ny = round(pop_adj_fak*10)
    nz = round(pop_adj_fak*10)

    mats = define_materials()
    define_environment(mats)
    fmats_rgb = filter_mats(mats,["Red","Green","Blue"])
    fmats_bvs = filter_mats(mats,["Blood","Vessel","Stuff"])

    need_len = 20
    irad = 2
    orad = 2.5
    define_cube_of_cubes(fmats_bvs, nx,ny,nz, need_len, irad, orad)


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