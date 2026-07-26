#include "ncorr.h"
#include <fstream>
#include <iostream>
#include <string>

using namespace ncorr;

// Reusable template function to save arrays to CSV
template <typename ArrayType, typename RoiType>
bool save_to_csv(const std::string& filename, const ArrayType& data_array, const RoiType& disp_roi, int height, int width) {
    std::ofstream csv_file(filename);
    if (!csv_file.is_open()) {
        std::cerr << "Error: Could not open " << filename << " for writing.\n";
        return false;
    }

    for (int p1 = 0; p1 < height; ++p1) {
        for (int p2 = 0; p2 < width; ++p2) {
            // Write data or NaN replacement
            if (disp_roi(p1, p2)) {
                csv_file << data_array(p1, p2);
            } else {
                csv_file << "nan";
            }

            // Write comma for all elements except the last one in the row
            if (p2 < width - 1) {
                csv_file << ",";
            }
        }
        csv_file << "\n";
    }
    
    csv_file.close();
	std::cout << "Successfully exported data to " << filename << std::endl;
    return true;
}

// Function that performs DIC and strain analysis on two input image paths and saves fields to CSV
bool analyze_dic_and_strain(const std::string& ref_image_path, 
                            const std::string& cur_image_path, 
                            const std::string& roi_image_path,
							const std::string& output_base) {
	try {
		// Initialize DIC and strain information ---------------//
		DIC_analysis_input DIC_input;
		DIC_analysis_output DIC_output;
		strain_analysis_input strain_input;
		strain_analysis_output strain_output;

		// Set images
		std::vector<Image2D> imgs;
		imgs.push_back(ref_image_path);
		imgs.push_back(cur_image_path);
		
		// Find number of hardware threads
		unsigned int num_threads = std::thread::hardware_concurrency();
		if (num_threads == 0)
			num_threads = 1;

		std::cout << "Using " << num_threads << " thread" << (num_threads == 1 ? "" : "s") << "." << std::endl;
		
		// Set DIC_input
		DIC_input = DIC_analysis_input(imgs, 							// Images
							ROI2D(Image2D(roi_image_path).get_gs() > 0.5),		// ROI
							3,                                         		// scalefactor
							INTERP::QUINTIC_BSPLINE_PRECOMPUTE,			// Interpolation
							SUBREGION::CIRCLE,					// Subregion shape
							20,                                        		// Subregion radius
							num_threads,            // # of threads
							DIC_analysis_config::NO_UPDATE,				// DIC configuration for reference image updates
							true);							// Debugging enabled/disabled

		// Perform DIC_analysis    
		DIC_output = DIC_analysis(DIC_input);

		// Convert DIC_output to Eulerian perspective
		DIC_output = change_perspective(DIC_output, INTERP::QUINTIC_BSPLINE_PRECOMPUTE);

		// Set units of DIC_output (provide units/pixel)
		DIC_output = set_units(DIC_output, "mm", 0.2);

		// Set strain input
		strain_input = strain_analysis_input(DIC_input,
											DIC_output,
											SUBREGION::CIRCLE,					// Strain subregion shape
											5);						// Strain subregion radius
		
		// Perform strain_analysis
		strain_output = strain_analysis(strain_input); 	
			
		// Get the displacement field you want to access 
		Disp2D disp = DIC_output.disps.back();  

		// Get the corresponding v and u Array2Ds 
		const Array2D<double> &v_array = disp.get_v().get_array();  
		const Array2D<double> &u_array = disp.get_u().get_array();  

		// Get the corresponding ROI2D 
		ROI2D disp_roi = disp.get_roi(); 

		// Get data height and width
		int height = disp.data_height();
		int width = disp.data_width();

		// Call the function for both u and v arrays
		save_to_csv(output_base+"u.csv", u_array, disp_roi, height, width);
		save_to_csv(output_base+"v.csv", v_array, disp_roi, height, width);

		// Get the strain field you want to access 
		Strain2D strain = strain_output.strains.back();  

		// Get the corresponding eyy, exy, and exx Array2Ds 
		const Array2D<double> &eyy_array = strain.get_eyy().get_array();  
		const Array2D<double> &exy_array = strain.get_exy().get_array();  
		const Array2D<double> &exx_array = strain.get_exx().get_array(); 

		// Get the corresponding ROI2D 
		ROI2D strain_roi = strain.get_roi();  
		
		// Get data height and width
		height = strain.data_height();
		width = strain.data_width();

		// Call the function for eyy, exy, and exx arrays
		save_to_csv(output_base+"eyy.csv", eyy_array, strain_roi, height, width);
		save_to_csv(output_base+"exy.csv", exy_array, strain_roi, height, width);
		save_to_csv(output_base+"exx.csv", exx_array, strain_roi, height, width);

		return true;
	} catch (const std::exception& e) {
		std::cerr << "DIC analysis failed: " << e.what() << std::endl;
    	return false;
	}
}

int main() {
	const std::string roi_path = "images/roi.png";

	for (int m = 0; m <= 100; m += 5) {
		std::string ref_image =
            "images/ohtcfrp_00_m" + std::to_string(m) + "_t90.png";

        std::string cur_image =
            "images/ohtcfrp_11_m" + std::to_string(m) + "_t90.png";

        std::string output_prefix =
            "outputs/ohtcfrp_00_m" + std::to_string(m) +
            "_t90_vs_ohtcfrp_11_m" + std::to_string(m) + "_t90_";
		
		// Call the function with your specific image paths
		analyze_dic_and_strain(ref_image, cur_image, roi_path, output_prefix);
	}
    return 0;
}