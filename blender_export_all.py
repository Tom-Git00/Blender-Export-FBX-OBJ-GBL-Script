import bpy
import os


# --- O Operador (A lógica do botão) ---
class EXPORT_OT_MultiFormatButton(bpy.types.Operator):
    """Exporta a seleção atual para FBX, OBJ, e GLB de uma só vez."""
    bl_idname = "export.multi_format_button"  # ID único do operador
    bl_label = "Exportar (FBX, OBJ, GLB)"     # Texto do botão
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        # 1. Obter o caminho base (onde o .blend está guardado)
        blend_filepath = bpy.data.filepath
        if not blend_filepath:
            self.report({'ERROR'}, "Por favor, guarde o ficheiro .blend primeiro.")
            return {'CANCELLED'}
        
        # Remove a extensão .blend para obter o nome base
        # Ex: "C:\Projeto\MinhaCena.blend" -> "C:\Projeto\MinhaCena"
        base_path_no_ext = os.path.splitext(blend_filepath)[0]

        try:
            #FBX Export
            fbx_path = base_path_no_ext + ".fbx"
            
            bpy.ops.export_scene.fbx(
                filepath=fbx_path,

                # --- Settings Específicas FBX ---

                check_existing=False,
                use_selection=True,                 # Exportar apenas o selecionado
                apply_scale_options='FBX_SCALE_ALL',# Aplicar escala (bom para Unity/Unreal)
                object_types={'MESH', 'ARMATURE', 'EMPTY'}, # O que exportar
                use_mesh_modifiers=True,            # Aplicar modificadores
                bake_anim_use_nla_strips=False,     # Não usar NLA
                bake_anim_use_all_actions=False,    # Não exportar todas as actions
            )
            self.report({'INFO'}, f"Exportado: {os.path.basename(fbx_path)}")

        #Erros na exportação FBX
        except Exception as e:
            self.report({'ERROR'}, f"Falha na exportação FBX: {e}")
        
        try:
        
            #OBJ Export
            obj_path = base_path_no_ext + ".obj"
            
            bpy.ops.wm.obj_export(
                filepath=obj_path,

                # --- Settings Específicas OBJ ---

                check_existing=False,
                export_selected_objects=True,                 # Exportar apenas o selecionado
                apply_modifiers=True,            # Aplicar modificadores
                export_materials=True,                 # Criar ficheiro .mtl
                export_triangulated_mesh=True,                 # Triangular faces
            )
            self.report({'INFO'}, f"Exportado: {os.path.basename(obj_path)}")
        
        #Erros na exportação OBJ
        except Exception as e:
            self.report({'ERROR'}, f"Falha na exportação OBJ: {e}")

        try:
            #GLB Export
            glb_path = base_path_no_ext + ".glb"
            
            bpy.ops.export_scene.gltf(
                filepath=glb_path,
                # --- Settings Específicas GLB ---
                export_format='GLB',                # 'GLB' (binário) ou 'GLTF_SEPARATE'
                use_selection=True,                 # Exportar apenas o selecionado
                export_apply=True,                  # Aplicar modificadores
                export_draco_mesh_compression_enable=True, # Usar compressão (opcional)
                export_materials='EXPORT',          # Exportar materiais
                export_lights=False,                # Não exportar luzes
                export_cameras=False,               # Não exportar câmaras
            )
            self.report({'INFO'}, f"Exportado: {os.path.basename(glb_path)}")

        #Erros na exportação GLB
        except Exception as e:
            self.report({'ERROR'}, f"Falha na exportação: {e}")

        self.report({'INFO'}, "Exportação múltipla concluída!")
        return {'FINISHED'}


# --- O Painel (A UI na Sidebar) ---
class VIEW3D_PT_MultiExporterPanel(bpy.types.Panel):
    """Cria um Painel na Sidebar (N) da 3D View"""
    bl_label = "Exportador Rápido"       # Título do painel
    bl_idname = "VIEW3D_PT_multi_exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Meu Export"           # Nome da "Aba" no N-Panel

    def draw(self, context):
        layout = self.layout
        
        # Desenha o botão que chama o nosso operador
        layout.operator(EXPORT_OT_MultiFormatButton.bl_idname)


# --- Funções de Registo ---
# Lista de todas as classes que o add-on precisa de registar
classes = (
    EXPORT_OT_MultiFormatButton,
    VIEW3D_PT_MultiExporterPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    # Desregistar na ordem inversa para evitar problemas
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


# --- Permite que o script seja corrido diretamente do Text Editor ---
if __name__ == "__main__":
    register()