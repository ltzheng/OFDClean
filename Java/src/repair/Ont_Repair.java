package repair;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import FD.Ontology;
import main.AppMain;
import org.apache.jena.base.Sys;

public class Ont_Repair {

	
//	public Map<String, List<String>> getOntRepairCandidate(){
//		return eqOntCandidateMap;
//	}

	public void fixSense(List<List<String>> csvList, Ontology[] all_Ontologies, List<List<String>> ofdList) {
		// TODO Auto-generated method stub

		// fill in eqTupleMap
		getEquivalenceClass(csvList, ofdList);
		
		for (Map.Entry<String, List<String>> entry : AppMain.eqTupleMap.entrySet()) {
			 
//			System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue() + ", List length = " + entry.getValue().size());

			String RHSAttr = entry.getKey().split(",")[0];
			Map<String, Integer> senseCountMap = new HashMap();
			Map<String, List<String>> senseTupleMap = new HashMap();

			for (int i = 0; i < all_Ontologies.length; i++){
				System.out.println(all_Ontologies[i].name);
				Map<String, ArrayList<String>> map = all_Ontologies[i].map;

				int count = 0;
				if(all_Ontologies[i].name.equals(RHSAttr)){
//					List<String> ontCand = new ArrayList<String> ();
//					for (Map.Entry<String, ArrayList<String>> entry2 : map.entrySet()) {
//
//						System.out.println("Key = " + entry2.getKey() + ", Value = " + entry2.getValue() + ", List length = " + entry2.getValue().size());
//
//					}

//					System.out.println("name is:" + all_Ontologies[i].name);
//					System.out.println("sense is:" + all_Ontologies[i].sense);
//					System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue() + ", List length = " + entry.getValue().size());
					for (int j = 0; j < entry.getValue().size(); j ++){
						int ontCandCount = 0;
						if(map.containsKey(entry.getValue().get(j).split(",")[1])){
							count ++;
							ontCandCount ++;
						}else{
							for (Map.Entry<String, ArrayList<String>> entry2 : map.entrySet()) {						 
								if(entry2.getValue().contains(entry.getValue().get(j).split(",")[1])){
									count ++;
									ontCandCount ++;
								}
							}
						}
//						if (ontCandCount == 0){
//							
//							ontCand.add(entry.getValue().get(j));
//						}
					}				
					senseCountMap.put(all_Ontologies[i].sense, count);
//					senseTupleMap.put(all_Ontologies[i].sense, ontCand);
				}
				
			}
			
			
			List<Map.Entry<String,Integer>> list = new ArrayList(senseCountMap.entrySet());
		    Collections.sort(list, (o1, o2) -> (o1.getValue() - o2.getValue()));

		    AppMain.eqSenseMap.put(entry.getKey(), list.get(list.size()-1).getKey());
		    
//		    AppMain.eqOntCandidateMap.put(entry.getKey(), senseTupleMap.get(list.get(list.size()-1).getKey()));
		    
//			for (Map.Entry<String, List<String>> entry2 : eqOntCandidateMap.entrySet()) {
//			 
//				System.out.println("Key = " + entry2.getKey() + ", Value = " + entry2.getValue() + ", List length = " + entry2.getValue().size());
//	 
//			}
	 
		}

		
	}
	
	public void getEquivalenceClass(List<List<String>> csvList, List<List<String>> ofdList){
		
		for(int i = 0; i < ofdList.size(); i ++){
			String LHSLine = ofdList.get(i).get(0);  // left attribute of an ontology
			String LHS[] = LHSLine.split(",");
			String RHS = ofdList.get(i).get(1);  // right attribute of an ontology

			// csvList.get(0): column names
			for (int j = 1; j < csvList.size(); j++){
				String key = RHS;
				
				for (int k = 0; k < LHS.length; k++){
					key = key + "," + csvList.get(j).get(csvList.get(0).indexOf(LHS[k]));
				}
				
				if(!AppMain.eqTupleMap.containsKey(key)){
					List<String> tupleList = new ArrayList<String>();
					tupleList.add(csvList.get(j).get(0)+","+csvList.get(j).get(csvList.get(0).indexOf(RHS)).toLowerCase());
					AppMain.eqTupleMap.put(key, tupleList);
				}else{
					List<String> tupleList = AppMain.eqTupleMap.get(key);
					tupleList.add(csvList.get(j).get(0)+","+csvList.get(j).get(csvList.get(0).indexOf(RHS)).toLowerCase());
					AppMain.eqTupleMap.put(key, tupleList);
				}		

			}
			
		}
	
	}

}
