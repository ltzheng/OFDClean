package FD;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Ontology {

	//public Map<String, String> synMap=new HashMap<>();
	public Map<String, ArrayList<String>> map = new HashMap();
	public double threshold;
	public int isa_Threshold;
	public String sense;
	public String name;
	public Ontology_class ontology_class;
	public boolean Strict=false;
	public enum Ontology_class
	{
		syn,
		isa
	};
}
