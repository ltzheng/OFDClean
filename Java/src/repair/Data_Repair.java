package repair;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import FD.CloneUtils;
import FD.Graph;
import FD.Ontology;
import main.AppMain;

public class Data_Repair {
	public static Set<String> globaCorrectValueSet = new HashSet<String>();
	
	
	public void identifyErrors(Map<String, List<String>> eqTupleMap, Map<String, String> eqSenseMap, Ontology[] all_Ontologies){
		
		for (Map.Entry<String, List<String>> entry : eqTupleMap.entrySet()) {
			int m = 0;
			String firstline = entry.getValue().get(0).split(",")[1];
			for(int i = 0; i < entry.getValue().size(); i ++){
				if(!firstline.equals(entry.getValue().get(i).split(",")[1])){
					m = i;
					break;
				}
			}

			if (m != 0){
				String ontologyAttr = entry.getKey().split(",")[0];
				List<String> tuples = entry.getValue();
				String ontologySense = eqSenseMap.get(entry.getKey());
				Set<String> LCASet = new HashSet();
//				System.out.println(tuples);
				
				
				for (int i = 0; i < all_Ontologies.length; i++){
					
					if(ontologyAttr.equals(all_Ontologies[i].name) && ontologySense.equals(all_Ontologies[i].sense)){	
//						System.out.println(ontologyAttr+" "+ ontologySense);
//						System.out.println(all_Ontologies[i].isa_Threshold);
						Map<String, List<String>> ontRelationMap = getOntRelationMap(all_Ontologies[i].map);
						
//						for(Map.Entry<String, List<String>> entry1 : ontRelationMap.entrySet()){
//							System.out.println("Key = " + entry1.getKey() + ", Value = " + entry1.getValue());
//						}
//						
//						System.out.println("------------------------------------------------------------------");
						
						//save all the LCA node with the correct values
						LCASet = findLCA(tuples, ontRelationMap, all_Ontologies[i].isa_Threshold, ontologySense);
						AppMain.LCAMap.put(entry.getKey(), LCASet);
						
						for (int j = 0; j < tuples.size(); j ++){
//							System.out.println(tuples.get(j).split(",")[1]);
							int count = 0;
							String repairValue = null;
							for(String str: LCASet){
//								System.out.println(str);
								repairValue = str;
								if (!tuples.get(j).split(",")[1].equals(str)){
									count ++;
								}
							}
//							System.out.println(count);
//							System.out.println(tuples.size());
							if (count == LCASet.size()){
								AppMain.ontCandidateSet.add(ontologySense + "," + tuples.get(j).split(",")[1] + "," + repairValue);
							}
						}
//						System.out.println("------------------------------------------------------------------");
						
	//					List<Map.Entry<String,Integer>> list = new ArrayList(nodeCountMap.entrySet());
	//				    Collections.sort(list, (o1, o2) -> (o1.getValue() - o2.getValue()));
	//				    
	//				    eqViolationMap.put(entry.getKey(), list.get(list.size()-1).getKey());
						
					}
				}				
			}
		}
//		
//		for(Map.Entry<String, Set<String>> entry1 : AppMain.LCAMap.entrySet()){
//			System.out.println("Key = " + entry1.getKey() + ", Value = " + entry1.getValue());
//		}
//		System.out.println("-----------------------------------------------");
	}
	
	
	public int getMiniNumDataRepair(Map<String, List<String>> eqTupleMap, Map<String, String> eqSenseMap, Set<String> ontCandidateSet, Map<String, Set<String>> LCAMap){
		
		Map<String, List<String>> localEqTupleMap = CloneUtils.clone(eqTupleMap);
//		mapCopy(localEqTupleMap, eqTupleMap);
		Map<String, String> localEqSenseMap = eqSenseMap;
		Set<String> localOntCandidateSet = new HashSet();
		localOntCandidateSet.addAll(ontCandidateSet);
		Map<String, Set<String>> localLCAMap = LCAMap;		
		
//		System.out.println(ontCandidateSet.toString());
		//conflict graph
		int graphMaxSize = 10000;
		Graph graph = new Graph(graphMaxSize);
		
		for (Map.Entry<String, List<String>> entry : localEqTupleMap.entrySet()) {
			List<String> LCATupleList = new ArrayList<String>();
			List<String> nonLCATupleList = new ArrayList<String>();
			
			//change the candidate value to a repair value
			if(localOntCandidateSet != null){
				for(String str: localOntCandidateSet){
//					System.out.println(str);
					if(localEqSenseMap.get(entry.getKey()).equals(str.split(",")[0])){
						for(int i = 0; i < entry.getValue().size(); i ++){
							String tuple = entry.getValue().get(i);
							String id = tuple.split(",")[0];
							String value = tuple.split(",")[1];
							if(value.equals(str.split(",")[1])){
//								System.out.println(entry.getValue());
								entry.getValue().set(i, id+","+str.split(",")[2]);
//								System.out.println(entry.getValue());
//								System.out.println("--------------------");
							}
						}
					}
				}
			}
			
			for(int i = 0; i < entry.getValue().size(); i ++){
				String tuple = entry.getValue().get(i);
				String value = tuple.split(",")[1];
				if(localLCAMap.get(entry.getKey()) != null){
					if(localLCAMap.get(entry.getKey()).contains(value)){
						LCATupleList.add(tuple);
					}else{
						nonLCATupleList.add(tuple);
					}
				}
			}
			
//			System.out.println(LCATupleList.size()+" "+nonLCATupleList.size());
			
//			for(int i = 0; i < LCATupleList.size(); i++){
//				System.out.println(LCATupleList.get(i));
//			}
//			
//			for(int i = 0; i < nonLCATupleList.size(); i++){
//				System.out.println(LCATupleList.get(i));
//			}
			
			for (int i = 0; i < LCATupleList.size(); i++){
				int v = Integer.parseInt(LCATupleList.get(i).split(",")[0]);
				
				if (nonLCATupleList.size() > 0){
					for(int j = 0; j < nonLCATupleList.size(); j++){
//						System.out.println(nonLCATupleList.get(j));
						int w = Integer.parseInt(nonLCATupleList.get(j).split(",")[0]);
						graph.addEdge(v, w);
					}
				}					
			}
			
			if (nonLCATupleList.size() > 1){
				for (int i = 0; i < nonLCATupleList.size(); i ++){
					int v = Integer.parseInt(LCATupleList.get(i).split(",")[0]);
					for(int j = i+1; j < nonLCATupleList.size(); j++){
						if(!nonLCATupleList.get(i).split(",")[1].equals(nonLCATupleList.get(j).split(",")[1])){
							int w = Integer.parseInt(nonLCATupleList.get(j).split(",")[0]);
							graph.addEdge(v, w);
						}
					}
				}
			}			
		}
		
//		System.out.println(graph.getVertexCover());
		return graph.getVertexCover();
		
	}
	
	public Set<String> findLCA(List<String> tuples, Map<String, List<String>> ontRelationMap, int isa_threshold, String sense){
		Map<String, Integer> nodeCountMap = new HashMap();
		Map<String, Set<String>> correctValueMap = new HashMap();
//		Map<String, Set<String>> results = new HashMap();
		Set<String> set = new HashSet();
		
		for(Map.Entry<String, List<String>> entry : ontRelationMap.entrySet()){
			nodeCountMap.put(entry.getKey(), visitNode(ontRelationMap, entry.getKey(), tuples, isa_threshold));
			set.addAll(globaCorrectValueSet);
			correctValueMap.put(entry.getKey(), set);
			globaCorrectValueSet.clear();
		}
		
		
		List<Map.Entry<String,Integer>> list = new ArrayList(nodeCountMap.entrySet());
		Collections.sort(list, (o1, o2) -> (o1.getValue() - o2.getValue()));
		
//		results.put(list.get(list.size()-1).getKey(), correctValueMap.get(list.get(list.size()-1).getKey()));
//		System.out.println(list.get(list.size()-1).getKey());
		 
		return correctValueMap.get(list.get(list.size()-1).getKey());
	}
	
	public int visitNode(Map<String, List<String>> ontRelationMap, String key, List<String> tuples, int isa_threshold){
//		for(Map.Entry<String, List<String>> entry : ontRelationMap.entrySet()){
//			System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue() + ", List length = " + entry.getValue().size());
//		}
//		System.out.println(key);
		
		int count = 0;
		List<String> list = ontRelationMap.get(key);
		for(int i = 0; i < list.size(); i ++){
			count = count + countForOneOntList(ontRelationMap, key, tuples);
		}
		while (isa_threshold != 0){
			isa_threshold --;
			for(int i = 0; i < list.size(); i ++){
//				System.out.println(list.get(i));
				if(ontRelationMap.containsKey(list.get(i))){
					count = count + visitNode(ontRelationMap, list.get(i), tuples, isa_threshold);
					
				}
			}
		}
		return count;
	}
	
	private int countForOneOntList(Map<String, List<String>> ontRelationMap, String key, List<String> tuples) {
//		System.out.println(key);
		// TODO Auto-generated method stub
		int count = 0;
//		System.out.println(tuples);
//		for(Map.Entry<String, List<String>> entry1 : ontRelationMap.entrySet()){
//			System.out.println("Key = " + entry1.getKey() + ", Value = " + entry1.getValue());
//		}

		for (int i = 0; i < tuples.size(); i++){
			if (key.equals(tuples.get(i).split(",")[1])){
				globaCorrectValueSet.add(key);
				count ++;
			}else {
				int num = 0;
				List<String> list = ontRelationMap.get(key);
				for(int j = 0; j < list.size(); j++){
					if(list.get(j).equals(tuples.get(i).split(",")[1])){
						globaCorrectValueSet.add(list.get(j));
						count ++;
						break;
					}
				}
			}			
		}
		
			
		return count;
	}

	public Map<String, List<String>> getOntRelationMap (Map<String, ArrayList<String>> map){
		Map<String, List<String>> ontRelationMap = new HashMap();
		
		for (Map.Entry<String, ArrayList<String>> entry : map.entrySet()) {
			List<String> list = new ArrayList<String>();
			if(!ontRelationMap.containsKey(entry.getValue().get(0))){
				list.add(entry.getKey());
				ontRelationMap.put(entry.getValue().get(0), list);
			}else{
				list = ontRelationMap.get(entry.getValue().get(0));
				list.add(entry.getKey());
				ontRelationMap.put(entry.getValue().get(0), list);
			}
//			System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue() + ", List length = " + entry.getValue().size());
		}
		
		
//		System.out.println("-------------------------------------------------------");
//		
//		for (Map.Entry<String, List<String>> entry : ontRelationMap.entrySet()){
//			System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue() + ", List length = " + entry.getValue().size());
//		}
//		
//		System.out.println("*******************************************************");
		
		return ontRelationMap;
		
	}
	

}
