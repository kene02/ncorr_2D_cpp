#include "ncorr.h"
#include <fstream>
#include <iostream>

using namespace ncorr;

int main() {
	// Initialize DIC and strain information ---------------//
	DIC_analysis_input DIC_input;
	DIC_analysis_output DIC_output;
	strain_analysis_input strain_input;
	strain_analysis_output strain_output;

	// Set images
	std::vector<Image2D> imgs;

	// Reference image
	std::ostringstream ostr;
	ostr << "images/ohtcfrp_00.png";
	imgs.push_back(ostr.str());

	ostr.str(""); // Clear previous buffer content
	ostr.clear(); // Reset error flags

	// Current image
	ostr << "images/ohtcfrp_11.png";
	imgs.push_back(ostr.str());

	// Set DIC_input
	DIC_input = DIC_analysis_input(imgs, 							// Images
						ROI2D(Image2D("images/roi.png").get_gs() > 0.5),		// ROI
						3,                                         		// scalefactor
						INTERP::QUINTIC_BSPLINE_PRECOMPUTE,			// Interpolation
						SUBREGION::CIRCLE,					// Subregion shape
						20,                                        		// Subregion radius
						4,                                         		// # of threads
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

	// Cycle over Disp2D and print out values  
	for (int p2 = 0; p2 < disp.data_width(); ++p2) {  
		for (int p1 = 0; p1 < disp.data_height(); ++p1) {  
			if (disp_roi(p1,p2)) {  
				std::cout << "v(" << p1 << "," << p2 << ") = " << v_array(p1,p2) << std::endl;  
				std::cout << "u(" << p1 << "," << p2 << ") = " << u_array(p1,p2) << std::endl;  
			}  
		}  
	}  
	// Open the CSV files for writing
	std::ofstream csv_file("outputs/u.csv");
	if (csv_file.is_open()) {
		// Cycle over Disp2D and save values 
		for (int p1 = 0; p1 < disp.data_height(); ++p1) { 
			for (int p2 = 0; p2 < disp.data_width(); ++p2) { 
				if (disp_roi(p1, p2)) { 
					csv_file << u_array(p1, p2);
				} else {
					csv_file << "nan";
				}
				csv_file << ",";
			}
			csv_file << "\n";
		}
		csv_file.close();
	} else {
		std::cerr << "Error: Could not open outputs/u.csv for writing." << std::endl;
	}

	std::ofstream csv_file("outputs/v.csv");
	if (csv_file.is_open()) {
		// Cycle over Disp2D and save values 
		for (int p1 = 0; p1 < disp.data_height(); ++p1) { 
			for (int p2 = 0; p2 < disp.data_width(); ++p2) { 
				if (disp_roi(p1, p2)) { 
					csv_file << v_array(p1, p2);
				} else {
					csv_file << "nan";
				}
				csv_file << ",";
			}
			csv_file << "\n";
		}
		csv_file.close();
	} else {
		std::cerr << "Error: Could not open outputs/v.csv for writing." << std::endl;
	}

	// Get the strain field you want to access 
	Strain2D strain = strain_output.strains.back();  

	// Get the corresponding eyy, exy, and exx Array2Ds 
	const Array2D<double> &eyy_array = strain.get_eyy().get_array();  
	const Array2D<double> &exy_array = strain.get_exy().get_array();  
	const Array2D<double> &exx_array = strain.get_exx().get_array(); 

	// Get the corresponding ROI2D 
	ROI2D strain_roi = strain.get_roi();  

	// Cycle over Strain2D and print out values  
	for (int p2 = 0; p2 < strain.data_width(); ++p2) {  
		for (int p1 = 0; p1 < strain.data_height(); ++p1) {  
			if (strain_roi(p1,p2)) {  
				std::cout << "eyy(" << p1 << "," << p2 << ") = " << eyy_array(p1,p2) << std::endl;  
				std::cout << "exy(" << p1 << "," << p2 << ") = " << exy_array(p1,p2) << std::endl;  
				std::cout << "exx(" << p1 << "," << p2 << ") = " << exx_array(p1,p2) << std::endl;  
			}
		}
	}

  	return 0;
}