#include "ncorr.h"

using namespace ncorr;

int main(int argc, char *argv[]) {
	if (argc != 2) {
		throw std::invalid_argument("Must have 1 command line input of either 'calculate' or 'load'");	
	}

	// Initialize DIC and strain information ---------------//
	DIC_analysis_input DIC_input;
	DIC_analysis_output DIC_output;
	strain_analysis_input strain_input;
	strain_analysis_output strain_output;

	// Determine whether or not to perform calculations or 
	// load data (only load data if analysis has already 
	// been done and saved or else throw an exception).
	std::string input(argv[1]);
	if (input == "load") {
		// Load inputs
		DIC_input = DIC_analysis_input::load("save/DIC_input.bin");
		DIC_output = DIC_analysis_output::load("save/DIC_output.bin");
		strain_input = strain_analysis_input::load("save/strain_input.bin");
		strain_output = strain_analysis_output::load("save/strain_output.bin");
	} else if (input == "calculate") {
		// Set images
		std::vector<Image2D> imgs;
		/*
		for (int i = 0; i <= 11; ++i) {
		    std::ostringstream ostr;
		    ostr << "images/ohtcfrp_" << std::setfill('0') << std::setw(2) << i << ".png";
		    imgs.push_back(ostr.str());
		}
		*/
		// Reference image
		std::ostringstream ostr;
		ostr << "images/ohtcfrp_00.png";
		imgs.push_back(ostr.str());

		/*
		// First loop: 0 to 20 in steps of 5
		for (int i = 0; i <= 20; i += 5) {
			std::ostringstream ostr;
			ostr << "images/ohtcfrp_11_m" << i << "_t90.png";
			imgs.push_back(ostr.str());
		}

		// Second loop: 40 to 100 in steps of 20
		for (int i = 40; i <= 100; i += 20) {
			std::ostringstream ostr;
			ostr << "images/ohtcfrp_11_m" << i << "_t90.png";
			imgs.push_back(ostr.str());
		}
		*/
		ostr.str(""); // Clear previous buffer content
		ostr.clear(); // Reset error flags

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
		
		// Save outputs as binary
                save(DIC_input, "save/DIC_input.bin");
                save(DIC_output, "save/DIC_output.bin");
                save(strain_input, "save/strain_input.bin");
                save(strain_output, "save/strain_output.bin");
	} else {
		throw std::invalid_argument("Input of " + input + " is not recognized. Must be either 'calculate' or 'load'");	
	}		
        
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