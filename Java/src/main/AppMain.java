package main;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import FD.FileFormat;
import FD.OFD;
import FD.Ontology;
import FD.ReadConfig;
import org.apache.jena.base.Sys;
import repair.Data_Repair;
import repair.Ont_Repair;
import FD.Data;
import FD.Graph;


public class AppMain {
	//save the eq, key is the LHS value of eq, value is all the tuples along with their values
	public static Map<String, List<String>> eqTupleMap = new HashMap();
	
	//save the fixed sense for each eq, key is the LHS value of eq, value is the sense
	public static Map<String, String> eqSenseMap = new HashMap();
	
//	//save all the ontology repair candidate for each eq, key is the LHS value of eq, value is the tuples along with their value that are not in the ontology
//	public static Map<String, List<String>> eqOntCandidateMap = new HashMap();
	
	//key is the LHS value of eq, value is the set of values that the LCA covers
	public static Map<String, Set<String>> LCAMap = new HashMap();
	
	public static Set<String> ontCandidateSet = new HashSet();
	

	
	//main function
	public static void main(String[] args) throws Exception {

		if (args.length != 2) {
			System.out
					.println("Please provide two inputs, one XML file and one directory to write the details.");
			return;
		}

		boolean write_Details = true;
		String configPath = args[0];// args[0];//
		String savingDirectory = args[1];// args[1];//
//		long start = System.currentTimeMillis();
		long start = System.nanoTime();
		long total = 0;

		ReadConfig RF = new ReadConfig();

		List<List<String>> csvList;
		List<List<String>> ofdList;

		Ontology[] all_Ontologies = RF.getOntology(configPath);
		if (RF.Error) {
			System.out.println("There are some Errors, Check the Log file");
			errorReport("rdf-error", savingDirectory);
			return;
		}
		Data dataconfig = RF.getDataConfig(configPath);

		csvList = FileFormat.csvInput(",", dataconfig.path);

		OFD ofdconfig = RF.getOFDConfig(configPath);
		
		ofdList = FileFormat.ofdInput("->", ofdconfig.path);

		Ont_Repair ontrep = new Ont_Repair();
		
		//fix sense for each eq, save candidates in the map
		// initial sense assignment
		ontrep.fixSense(csvList, all_Ontologies, ofdList);
		
		Data_Repair datarepair = new Data_Repair();

		datarepair.identifyErrors(AppMain.eqTupleMap, AppMain.eqSenseMap, all_Ontologies);
		
		for(String str: ontCandidateSet){
			System.out.println(str);
		}

		long end = System.nanoTime();
		System.out.println("Took: " + ((end - start) / 1000000) + "ms");
		
//		System.out.println("------------------------------------------------------------------");
		
//		Set<String> set1 = new HashSet();
//		set1.add("EU,cele,celebrex");
//		set1.add("Disease,cholesterol,high_cholesterol");
//		set1.add("EU,lexapr,loxitane");
//		set1.add("Disease,cholesterol,hypercholesterolemia");
//		set1.add("EU,coza,simovil");
//		set1.add("EU,lepro,loxitane");
		
		
//		getPretoOptimalSolution(datarepair, 3);
//		System.out.println(datarepair.getMiniNumDataRepair(AppMain.eqTupleMap, AppMain.eqSenseMap, set1, AppMain.LCAMap));
//		
//		Set<String> set2 = new HashSet();
//		set2.add("EU,cele,celebrex");
//		System.out.println(datarepair.getMiniNumDataRepair(AppMain.eqTupleMap, AppMain.eqSenseMap, set2, AppMain.LCAMap));
		
		
//		ontrep.getOntRepairCandidate();
		
//		for (int i = 0; i < all_Ontologies.length; i++){
//			Map<String, ArrayList<String>> map = all_Ontologies[i].map;
//			System.out.println("name is:" + all_Ontologies[i].name);
//			System.out.println("class is:" + all_Ontologies[i].ontology_class);
//			System.out.println("sense is:" + all_Ontologies[i].sense);
//			System.out.println("Is_a threshold is: " + all_Ontologies[i].isa_Threshold);
//			for (Map.Entry<String, ArrayList<String>> entry : map.entrySet()) {
//				 
//			    System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue() + ", List length = " + entry.getValue().size());
//			 
//			}
//			System.out.println("------------------------------------------------------");
//		}
	}
	
	//get Preto-optimal solutions
	public static void getPretoOptimalSolution(Data_Repair datarepair, int beta){
		
		Map<Set<String>, Integer> solutionMap = new HashMap();
		Map<Set<String>, Integer> beamSearchMap = new HashMap();
		List<Set<Set<String>>> list = new ArrayList();
		List<Set<Set<String>>> beamSearchList = new ArrayList();
		
//		Set<String> set = new HashSet();
//		set.add("EU,cele,celebrex");
//		set.add("Disease,cholesterol,high_cholesterol");
//		set.add("EU,lexapr,loxitane");
//		set.add("Disease,cholesterol,hypercholesterolemia");
//		set.add("EU,coza,simovil");
//		set.add("EU,lepro,loxitane");
		
		
//		getPretoOptimalSolution(datarepair);
//		System.out.println(datarepair.getMiniNumDataRepair(AppMain.eqTupleMap, AppMain.eqSenseMap, set, AppMain.LCAMap));

		if(AppMain.ontCandidateSet.size() == 0 || AppMain.ontCandidateSet == null){
			System.out.println("It is a clean dataset!");
		}else{
			for (int i = 0; i < AppMain.ontCandidateSet.size(); i++){
				Set<Set<String>> outerSet = new HashSet();
				Map<Set<String>, Integer> map = new HashMap();
				if(i == 0){
					solutionMap.put(null, datarepair.getMiniNumDataRepair(AppMain.eqTupleMap, AppMain.eqSenseMap, AppMain.ontCandidateSet, AppMain.LCAMap));
					for (String str: AppMain.ontCandidateSet){
						Set<String> innerSet = new HashSet();
						innerSet.add(str);
						outerSet.add(innerSet);
						map.put(innerSet, datarepair.getMiniNumDataRepair(AppMain.eqTupleMap, AppMain.eqSenseMap, innerSet, AppMain.LCAMap));
					}
//					beamSearchList.add(outerSet);
//					for (Entry<Set<String>, Integer> entry : map.entrySet()) {
//						 
//					    System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
//					 
//					}
					
					
					List<Map.Entry<Set<String>,Integer>> tempList = new ArrayList(map.entrySet());
				    Collections.sort(tempList, (o1, o2) -> (o1.getValue() - o2.getValue()));
				    
				    solutionMap.put(tempList.get(0).getKey(), tempList.get(0).getValue());
				    
				    Set<Set<String>> tempSet = new HashSet();
				    for (int k = 0; k < beta; k ++){  	
				    	if (k < tempList.size()){
				    		beamSearchMap.put(tempList.get(k).getKey(), tempList.get(k).getValue());
				    		tempSet.add(tempList.get(k).getKey());
				    	}else{
				    		for (int j = 0; j < tempList.size(); j++){
				    			beamSearchMap.put(tempList.get(j).getKey(), tempList.get(j).getValue());
					    		tempSet.add(tempList.get(j).getKey());
				    		}
				    	}
				    }
				    
				    beamSearchList.add(tempSet);
				    
//				    for (Entry<Set<String>, Integer> entry : beamSearchMap.entrySet()) {
//						 
//					    System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
//					 
//					}
//				    
//				    System.out.println("------------------------------------------------------");
				    
//					System.out.println(list.get(i));
					continue;
				}else{				
					for (String str: AppMain.ontCandidateSet){
						for (Set<String> set: beamSearchList.get(i-1)){
							if(!set.contains(str)){
								Set<String> tempSet = new HashSet();
								tempSet.addAll(set);
								tempSet.add(str);
								outerSet.add(tempSet);
//								System.out.println(tempSet.toString());
//								Set<String> aset = new HashSet();
//								aset.add("EU,cele,celebrex");
//								aset.add("Disease,cholesterol,high_cholesterol");
								map.put(tempSet, datarepair.getMiniNumDataRepair(AppMain.eqTupleMap, AppMain.eqSenseMap, tempSet, AppMain.LCAMap));
							}
						}
						
					}
					
//					beamSearchList.add(outerSet);
//					System.out.println(list.get(i));
					
//					for (Entry<Set<String>, Integer> entry : map.entrySet()) {
//						 
//					    System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
//					 
//					}
//					System.out.println("*****************************************");
					
					List<Map.Entry<Set<String>,Integer>> tempList = new ArrayList(map.entrySet());
				    Collections.sort(tempList, (o1, o2) -> (o1.getValue() - o2.getValue()));
				    
				    solutionMap.put(tempList.get(0).getKey(), tempList.get(0).getValue());				   
				    
				    Set<Set<String>> tempSet = new HashSet();
				    for (int k = 0; k < beta; k ++){  	
				    	if (k < tempList.size()){
				    		beamSearchMap.put(tempList.get(k).getKey(), tempList.get(k).getValue());
				    		tempSet.add(tempList.get(k).getKey());
				    	}else{
				    		for (int j = 0; j < tempList.size(); j++){
				    			beamSearchMap.put(tempList.get(j).getKey(), tempList.get(j).getValue());
					    		tempSet.add(tempList.get(j).getKey());
				    		}
				    	}
				    }
				    
				    beamSearchList.add(tempSet);
				    
//				    for (Entry<Set<String>, Integer> entry : beamSearchMap.entrySet()) {
//						 
//					    System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
//					 
//					}
//				    
//					System.out.println("------------------------------------------------------");
				}
				
			}
		}
		
		System.out.println("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");
		for (Entry<Set<String>, Integer> entry : solutionMap.entrySet()) {
			 System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
		}
		System.out.println("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");
		
	}
	
	public static void errorReport(String keyword, String path)
			throws FileNotFoundException {
		String error = "";
		if (keyword.equals("rdf-error")) {
			error = "@";
		}
		PrintWriter pw = new PrintWriter(new File(path + "output.txt"));
		pw.write(error);
		pw.close();
	}
}
