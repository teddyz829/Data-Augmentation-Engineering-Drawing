import ezdxf
import sys
'''
IO stream for dxf files 
'''

class streamIO:

	def __init__(self, doc=None, msp=None, filename=None):
		self.doc = doc
		self.msp = msp
		self.filename = filename

	def create_doc(self, version_name='AC1015'):
		self.doc = ezdxf.new(version_name)

		self.doc.header['$LIMMIN'] = (0,0)
		self.doc.header['$LIMMAX'] = (512,512)


		self.msp = self.doc.modelspace()

	def load_doc(self):
		if self.filename:
			self.doc = ezdxf.readfile(self.filename)
			self.msp = self.doc.modelspace()
		else:
			print("No file found! Create a new file...")
			self.create_doc()

	def create_layers(self):
		self.doc.styles.new('Regular',
					   dxfattribs={'font': 'OpenSans-Regular.ttf'})
		self.doc.styles.new('Times',
					   dxfattribs={'font': 'times.ttf'})
		self.doc.styles.new('Candara',
					   dxfattribs={'font': 'Candara.ttf'})
		self.doc.styles.new('Arial',
					   dxfattribs={'font': 'arial.ttf'})
		my_line_types = [
			(
			"DOTTED", "Dotted .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .",
			[0.2, 0.0, -0.2]),
			("DOTTEDX2", "Dotted (2x) .    .    .    .    .    .    .    . ",
			 [0.4, 0.0, -0.4]),
			("DOTTED2", "Dotted (.5) . . . . . . . . . . . . . . . . . . . ",
			 [0.1, 0.0, -0.1]),
			("D", "-	-	-	-	-	-	-	-	-	",
			 [1.0, 0.9, -1.0]),
		]
		for name, desc, pattern in my_line_types:
			if name not in self.doc.linetypes:
				self.doc.linetypes.new(name=name, dxfattribs={'description': desc,
														 'pattern': pattern})

		## Contour: 1. Line    2. Circle    3. Arc    4. Dashed_line
		## 'color': 1 => red; 102 => green; 5=> blue
		if 'CONTOUR_LINE' not in self.doc.layers:
			self.doc.layers.new(name='CONTOUR_LINE', dxfattribs={'linetype': 'Continuous'})
		if 'CONTOUR_CIRCLE' not in self.doc.layers:
			self.doc.layers.new(name='CONTOUR_CIRCLE', dxfattribs={'linetype': 'Continuous'})
		if 'CONTOUR_ARC' not in self.doc.layers:
			self.doc.layers.new(name='CONTOUR_ARC', dxfattribs={'linetype': 'Continuous'})
		if 'CONTOUR_DASH' not in self.doc.layers:
			self.doc.layers.new(name='CONTOUR_DASH', dxfattribs={'linetype': 'D'})

		## Construction:
		if 'CONSTRUCTION' not in self.doc.layers:
			self.doc.layers.new(name='CONSTRUCTION', dxfattribs={'linetype': 'Continuous'})
		if 'DIMENSION' not in self.doc.layers:
			self.doc.layers.new(name='DIMENSION', dxfattribs={'linetype': 'Continuous'})

	def saveDXF(self, savename=None):
		if savename:
			self.doc.saveas(savename)
		else:
			self.doc.saveas(self.filename)

#
# if __name__ == "__main__":
# 	stream1 = streamIO(filename=sys.argv[1])
# 	stream1.create_doc()
# 	# stream1.load_doc()
# 	stream1.create_layers()
# 	stream1.saveDXF()