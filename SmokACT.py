#the script for generating the Smok ACT project
#move into the root next to your other project generation python scripts
#or tweak the "sys.path.insert(1, "BTDScripts")"
#or make any other tweaks this is all yours :3

import sys

sys.path.insert(1, "BTDScripts")
import Dep_FMT
import Dep_GLM
import Dep_STB
import Dep_SDL
import Dep_Vulkan
import Dep_ImGUI

import PremakeGenerate as PremakeGen
import Premake_Defines
import Premake_Links
import Premake_BuildOptions
import Premake_Flags

import Smok
import BTDSTD
import Wireframe

#defines the link name
PROJECT_NAME = "SmokACT"

#defines the include directory
PROJECT_INCLUDE_DIR = "SmokACT/includes"

def GeneratePremake():
    premakeCode = ""

    #KAR main exe project
    KARProject = PremakeGen.Project()
    KARProject.name = PROJECT_NAME
    KARProject.kind = "StaticLib"
    KARProject.language = "C++"
        
    KARProject.location = "SmokACT"
    KARProject.desc = "The Smok Asset Convertion Toolkit, used to convert other meshes and assets to formats optimized for Smok."

    KARProject.binaryOutput = PremakeGen.GenerateDefaultBinaryOutputPath() + "/BTDSDK"

    premakeCode = premakeCode + KARProject.GenerateProjectHeaderString()

    KARProject.sourceFiles = []
    premakeCode = premakeCode + KARProject.GenerateProjectSourceString()

    KARProject.includeDirs = {Dep_SDL.SDL_INCLUDE_DIR,
Dep_FMT.FMT_INCLUDE_DIR, Dep_GLM.GLM_INCLUDE_DIR, Dep_STB.STB_INCLUDE_DIR,
Dep_Vulkan.VMA_INCLUDE_DIR, Dep_Vulkan.VK_BOOTSTRAP_INCLUDE_DIR, Dep_Vulkan.VULKAN_INCLUDE_DIR, Dep_ImGUI.IMGUI_INCLUDE_DIR,
    "Venders/assimp/include", "Venders/assimp/Build/include", BTDSTD.PROJECT_INCLUDE_DIR,
    Smok.PROJECT_INCLUDE_DIR, Wireframe.PROJECT_INCLUDE_DIR}
    premakeCode = premakeCode + KARProject.GenerateProjectIncludeString()

    premakeCode = premakeCode + Premake_Links.GenerateLinksString({Dep_Vulkan.VULKAN_LINK_DIR, Smok.PROJECT_NAME})

    premakeCode = premakeCode + Premake_Defines.GenerateDefinesString({
    "GLM_FORCE_RADIANS",
    "GLM_FORCE_DEPTH_ZERO_TO_ONE",
    "GLM_ENABLE_EXPERIMENTAL"
})

    premakeCode = premakeCode + Premake_Flags.GenerateFlagsString({"NoRuntimeChecks",
    "MultiProcessorCompile"})

    premakeCode = premakeCode + Premake_BuildOptions.GenerateBuildOptionFlagsString({"/utf-8"})

    premakeCode = premakeCode + """

--platforms
filter "system:windows"
    cppdialect "C++20"
    staticruntime "On"
    systemversion "latest"
"""

    premakeCode = premakeCode + Premake_Defines.GenerateDefinesString({"Window_Build",
        "Desktop_Build",
        "VK_USE_PLATFORM_WIN32_KHR"})

    premakeCode = premakeCode + """
filter "system:linux"
    cppdialect "C++20"
    staticruntime "On"
    systemversion "latest"
"""

    premakeCode = premakeCode + Premake_Defines.GenerateDefinesString({"Linux_Build",
        "Desktop_Build",
        "VK_USE_PLATFORM_XLIB_KHR"})

    premakeCode = premakeCode + """

    filter "system:mac"
    cppdialect "C++20"
    staticruntime "On"
    systemversion "latest"
"""

    premakeCode = premakeCode + Premake_Defines.GenerateDefinesString({"MacOS_Build",
        "Desktop_Build",
        "VK_USE_PLATFORM_MACOS_MVK"})

    premakeCode = premakeCode + """
--configs
filter "configurations:Debug"
    defines "BTD_DEBUG"
    symbols "On"
"""

    premakeCode = premakeCode + Premake_Links.GenerateLinksString({Dep_SDL.SDL_VERSION_DEBUG_LINK_FILEPATH,
    "Venders/assimp/Build/lib/RelWithDebInfo/assimp-vc143-mt.lib", "Venders/assimp/Build/lib/RelWithDebInfo/draco.lib"})

    premakeCode = premakeCode + """
filter "configurations:Release"
    defines "BTD_RELEASE"
    optimize "On"

"""

    premakeCode = premakeCode + Premake_Links.GenerateLinksString({Dep_SDL.SDL_VERSION_RELEASE_LINK_FILEPATH,
    "Venders/assimp/Build/lib/Release/assimp-vc143-mt.lib", "Venders/assimp/Build/lib/Release/draco.lib"})

    premakeCode = premakeCode + """
filter "configurations:Dist"
    defines "BTD_DIST"
    optimize "On"
"""

    premakeCode = premakeCode + Premake_Defines.GenerateDefinesString({"NDEBUG"})
    premakeCode = premakeCode + Premake_Flags.GenerateFlagsString({"LinkTimeOptimization"})

    premakeCode = premakeCode + Premake_Links.GenerateLinksString({Dep_SDL.SDL_VERSION_DIST_LINK_FILEPATH,
    "Venders/assimp/Build/lib/MinSizeRel/assimp-vc143-mt.lib", "Venders/assimp/Build/lib/MinSizeRel/draco.lib"})


    return premakeCode