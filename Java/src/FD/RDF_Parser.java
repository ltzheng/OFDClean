package FD;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.rdf.model.Statement;
import org.apache.jena.rdf.model.StmtIterator;

import FD.Ontology.Ontology_class;

public class RDF_Parser {

	public boolean ReadRDFFile(String rdfPath, Ontology ontology)
	{
		final String dcat = "http://example.org/";
	    Model model = ModelFactory.createDefaultModel();
	    model.read(rdfPath);
	    StmtIterator iterator = model.listStatements();
		Map<String, ArrayList<String>> values=new HashMap<String, ArrayList<String>>();
	    while (iterator.hasNext()) {
			Statement stm = (Statement) iterator.next();
			Resource subject = (Resource) stm.getSubject();
			Property predicate = (Property) stm.getPredicate();
			RDFNode object = (RDFNode) stm.getObject();
			String []sub=subject.toString().split(dcat);
			String []pred=predicate.toString().split(dcat);
			String []obj=object.toString().split(dcat);
			String from = "",opt="",to="";
			if(sub.length==2)
				from=sub[1];
			if(pred.length==2)
				opt=pred[1];
			if(obj.length==2)
				to=obj[1];
			if(!from.equals("") && !to.equals(""))
			{
				from=from.trim().toLowerCase();
				to=to.trim().toLowerCase();
				if(!values.containsKey(from))
					values.put(from, new ArrayList<String>());
				values.get(from).add(to);
			}
		}
	    boolean ISA=ontology.ontology_class==Ontology_class.isa;
	    for (String key : values.keySet()) {
			if(values.get(key).size()>1)
				ISA=true;
		}
	    if(!ISA)
	    {
	    	for (String key : values.keySet()) {
				for (String val : values.get(key)) {
					if(values.containsKey(val))
					{
						ISA=true;
						break;
					}
				}
				if(ISA)
					break;
			}
	    }
	    if(ISA && ontology.ontology_class==Ontology_class.syn)
	    	return false;
	    if(ISA)
	    {
	    	for (String key : values.keySet()) {
	    		for (String val : values.get(key)) {
	    			if(values.containsKey(val))
	    			{
	    				for (String str : values.get(val)) {
	    					if(values.get(key).contains(str))
	    					{
	    						if(values.get(key).indexOf(val)>values.get(key).indexOf(str))
	    						{
	    							int start=values.get(key).indexOf(str);
	    							int end=values.get(key).indexOf(val);
	    							Collections.swap(values.get(key), start, end);
	    							for (int i = start+1; i < end; i++) {
	        							Collections.swap(values.get(key), i, end);									
									}
	    							
	    						}
	    					}
						}
	    			}
				}
			}
	    }
	    if(ISA)
	    {
	    	Map<String, ArrayList<String>> map2 =new HashMap<String, ArrayList<String>>();
	    	for (String key : values.keySet()) {
				for (int i = 0; i < values.get(key).size()-1; i++) {
					if(!map2.containsKey(values.get(key).get(i)))
					{
						ArrayList <String> al = new ArrayList<String>();
						for (int j = i+1; j < values.get(key).size(); j++) {
							al.add(values.get(key).get(j).toString().toLowerCase());	
						}
						map2.put(values.get(key).get(i).toString(), al);
					}
				}
			}
	    	for (String key : map2.keySet()) {
				if(!values.containsKey(key))
					values.put(key, map2.get(key));
			}
	    }
	    ontology.map=values;
	    if(!ISA)
	    {
	    	ArrayList<String> str = new ArrayList<String>();
	    	for (String key : ontology.map.keySet()) {
	    		for (String value : ontology.map.get(key)) {
	    			str.add(value);
				}
			}
			for (String key : str) {
				if (!ontology.map.containsKey(key))
				{
					ArrayList<String> temp=new ArrayList<String>();
					temp.add(key);
					ontology.map.put(key, temp);
				}
			}
	    }
	    return true;
	}
}
