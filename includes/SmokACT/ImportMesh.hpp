#pragma once

//Smok Asset Convertion Tool for turning mesh formats such as FBX, Obj, Collada, ect into Smok Mesh formats
//intergrates with Atomic (Smok's version of Nanite) to auto-gen LODs

#include <Smok/Mesh.hpp>

namespace Smok::AssetConvertionTool::Mesh
{
	//generates a material

	//imports a static mesh
	bool LoadStaticMesh(const char* rawMeshPath, Asset::Mesh::StaticMesh& staticMesh);

	//imports a animated mesh
}