package FD;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class FileFormat {
	//reads the given csv file and returns a two dimentional list representing the file. 
    public static List<List<String>> csvInput(String delim, String file) throws IOException{
        ArrayList<List<String>> csvList = new ArrayList<>();
        String lineString;
        ArrayList<String> line;
        BufferedReader br;
        
        br = new BufferedReader(new FileReader(new File(file)));
        while((lineString = br.readLine()) != null){
        	String []blabla=lineString.split(delim);
        	line=new ArrayList<String>();
        	for (String string : blabla) {
				line.add(string.replaceAll("\u00A0", ""));
			}
            //line = new ArrayList<String>(Arrays.asList(lineString.split(delim)));
            csvList.add(line);
        }
        br.close();
        return csvList;
    }
    
    public static List<List<String>> ofdInput(String delim, String file) throws IOException{
        ArrayList<List<String>> ofdList = new ArrayList<>();
        String lineString;
        ArrayList<String> line;
        BufferedReader br;
        
        br = new BufferedReader(new FileReader(new File(file)));
        while((lineString = br.readLine()) != null){
        	String []blabla=lineString.split(delim);
        	line=new ArrayList<String>();
        	for (String string : blabla) {
				line.add(string.replaceAll("\u00A0", ""));
			}
            //line = new ArrayList<String>(Arrays.asList(lineString.split(delim)));
            ofdList.add(line);
        }
        br.close();
        return ofdList;
    }
    
    //converts a two dimentional list into a Map of the attribute names to the values related to said attribute
    public static Map<String, List<String>> toMap(List<List<String>> csvList){
        Map<String, List<String>> finalMap = new HashMap<>();
        
        for(int i = 0; i<csvList.get(0).size(); i++){
            List<String> values = new ArrayList<>();
            for(int j = 1; j< csvList.size(); j++){
                values.add(csvList.get(j).get(i));
            }
            finalMap.put(csvList.get(0).get(i),values);
        }
        return finalMap;
    }
    
    //for each attribute in "columns" getEquiv finds all indexes with the same value associated to them, and adds them to a list.  
    //It then does this for all values in said column, and makes a list of the value lists.  The two dimentional list is returned for each value in a map
    public static Map<Set<String>, List<List<Integer>>> getEquiv(Map<String, List<String>> columns, Integer length, List<String> ontologyAttributes){
        Map<Set<String>, List<List<Integer>>> map = new HashMap<>();
        Iterator<Map.Entry<String,List<String>>> columnIt = columns.entrySet().iterator();
        List<Integer> temp = new ArrayList<>();             //temp is a list of all indexes that have already been added to an equiv list, prevents duplicating
        while(columnIt.hasNext()){
            List<List<Integer>> listOfValues = new ArrayList<>();
            Map.Entry<String,List<String>> entry = columnIt.next();
            String attribute = entry.getKey();
            List<String> column = entry.getValue();
            for(int i=0; i<column.size(); i++){
                List<Integer> values = new ArrayList<>();
                if(!temp.contains(i)){
                    values.add(i);
                    temp.add(i);
                    for(int j = i+1; j<column.size(); j++){
                        if(column.get(j).equals(column.get(i))){
                            values.add(j);
                            temp.add(j);
                        }
                    }
                    listOfValues.add(values);
                }
            }
            temp.clear();
            if(listOfValues.size()<length || ontologyAttributes.contains(attribute)){   //if the attribute is a key, it can be ignored through all calculations, since keys are not being considered
                Set<String> attSet = new HashSet<>();
                attSet.add(attribute);
                map.put(attSet,listOfValues);
            }
        }
        return map;
    }
}
