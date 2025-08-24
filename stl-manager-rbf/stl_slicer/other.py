# def get_slices_vertex_ids(mesh_vertex_projections_np: np.ndarray, slices_number: int, min_projection: float):
#     ''''''
#     slices_vertex_ids_list = []
#     # Get the vertex ids inside each slice
#     for slice_idx in range(slices_number):
#         slice_start = min_projection + (slice_idx * thickness)
#         slice_end = slice_start + thickness
        
#         # Get those vertex inside the slice
#         vertex_inside_slice_id_np = np.where((mesh_vertex_projections_np >= slice_start) &
#                                              (mesh_vertex_projections_np <= slice_end))[0]
        
#         slices_vertex_ids_list.append(vertex_inside_slice_id_np)
    
#     return slices_vertex_ids_list

# def get_slices_ranges(slices_number: int, min_projection: float):
#     '''Get slices minimum and maximum projected value'''
#     slices_ranges_list = []
#     for slice_idx in range(slices_number):
#         slice_start = min_projection + (slice_idx * thickness)
#         slice_end = slice_start + thickness
#         slices_ranges_list.append([slice_start, slice_end])
#     return np.array(slices_ranges_list)