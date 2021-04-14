package FD;


import java.io.File;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

public class ReadConfig {

//	public class dataConf {
//		public String path;
//		public int number_of_columns;
//		public boolean FastOFD = true;
//		public boolean SynOFD = false;
//		public boolean SynAOFD = false;
//		public boolean IsaOFD = false;
//		public boolean IsaAOFD = false;
//		public boolean Tane = false;
//	}
	
	public boolean Error=false;

	public Data getDataConfig(String path) {
		try {
			File fXmlFile = new File(path);
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory
					.newInstance();
			DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
			Document doc = dBuilder.parse(fXmlFile);

			doc.getDocumentElement().normalize();

			NodeList nList = doc.getElementsByTagName("data");

			Data conf = new Data();

			for (int temp = 0; temp < nList.getLength(); temp++) {

				Node nNode = nList.item(temp);

				if (nNode.getNodeType() == Node.ELEMENT_NODE) {

					Element eElement = (Element) nNode;
					conf.path = eElement.getElementsByTagName("path").item(0)
							.getTextContent();
					conf.number_of_columns = Integer.valueOf(eElement
							.getElementsByTagName("numberOfColumns").item(0)
							.getTextContent());
//					try {
//						conf.FastOFD = Boolean.valueOf(eElement
//								.getElementsByTagName("FastOFD").item(0)
//								.getTextContent());
//					} catch (Exception e) {
//					}
//					try {
//						conf.IsaAOFD = Boolean.valueOf(eElement
//								.getElementsByTagName("IsaAOFD").item(0)
//								.getTextContent());
//					} catch (Exception e) {
//					}
//					try {
//						conf.IsaOFD = Boolean.valueOf(eElement
//								.getElementsByTagName("IsaOFD").item(0)
//								.getTextContent());
//					} catch (Exception e) {
//					}
//					try {
//						conf.SynAOFD = Boolean.valueOf(eElement
//								.getElementsByTagName("SynAOFD").item(0)
//								.getTextContent());
//					} catch (Exception e) {
//					}
//					try {
//						conf.SynOFD = Boolean.valueOf(eElement
//								.getElementsByTagName("SynOFD").item(0)
//								.getTextContent());
//					} catch (Exception e) {
//					}
//					try {
//						conf.Tane = Boolean.valueOf(eElement
//								.getElementsByTagName("Tane").item(0)
//								.getTextContent());
//					} catch (Exception e) {
//					}
				}
			}

			return conf;
		} catch (Exception ex) {
			ex.printStackTrace();
			return null;
		}
	}
	
	public OFD getOFDConfig(String path) {
		try {
			File fXmlFile = new File(path);
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory
					.newInstance();
			DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
			Document doc = dBuilder.parse(fXmlFile);

			doc.getDocumentElement().normalize();

			NodeList nList = doc.getElementsByTagName("ofd");

			OFD conf = new OFD();

			for (int temp = 0; temp < nList.getLength(); temp++) {

				Node nNode = nList.item(temp);

				if (nNode.getNodeType() == Node.ELEMENT_NODE) {

					Element eElement = (Element) nNode;
					conf.path = eElement.getElementsByTagName("path").item(0)
							.getTextContent();
				}
			}

			return conf;
		} catch (Exception ex) {
			ex.printStackTrace();
			return null;
		}
	}

	public Ontology[] getOntology(String path) {
		try {
			File fXmlFile = new File(path);
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory
					.newInstance();
			DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
			Document doc = dBuilder.parse(fXmlFile);

			doc.getDocumentElement().normalize();

			NodeList nList = doc.getElementsByTagName("ontology");

			Ontology[] all_Ontologies = new Ontology[nList.getLength()];

			for (int temp = 0; temp < nList.getLength(); temp++) {

				Node nNode = nList.item(temp);

				if (nNode.getNodeType() == Node.ELEMENT_NODE) {

					Element eElement = (Element) nNode;

					Ontology ontology = new Ontology();
					RDF_Parser parser=new RDF_Parser();
					ontology.ontology_class = Ontology.Ontology_class
							.valueOf(eElement.getElementsByTagName("class")
									.item(0).getTextContent().toString());
					ontology.threshold = Double.valueOf(eElement
							.getElementsByTagName("threshold").item(0)
							.getTextContent());
					ontology.sense = eElement.getElementsByTagName("sense")
							.item(0).getTextContent();
					ontology.name = eElement.getElementsByTagName("name")
							.item(0).getTextContent();
					try {
						ontology.Strict = Boolean.valueOf(eElement
								.getElementsByTagName("strict").item(0)
								.getTextContent().toString());
					} catch (Exception e) {

					}
					try {
						ontology.isa_Threshold = Integer.valueOf(eElement
								.getElementsByTagName("isathreshold").item(0)
								.getTextContent().toString());
					} catch (Exception e) {

					}
					boolean res=parser.ReadRDFFile(eElement.getElementsByTagName("path").item(0).getTextContent(), ontology);
					if(!res)
					{
						Error=true;
						return null;
					}
					all_Ontologies[temp] = ontology;
				}
			}

			return all_Ontologies;
		} catch (Exception ex) {
			ex.printStackTrace();
			return null;
		}
	}

	public Ontology[] Create_Ontology_HashMap(Ontology[] ont, String key) {
		int counter = 0;
		for (int i = 0; i < ont.length; i++) {
			if (ont[i].name.equals(key))
				counter++;
		}
		if (counter == 0)
			return null;
		else {
			int index = 0;
			Ontology[] ret = new Ontology[counter];
			for (int i = 0; i < ont.length; i++) {
				if (ont[i].name.equals(key))
					ret[index++] = ont[i];
			}
			return ret;
		}
	}
}
