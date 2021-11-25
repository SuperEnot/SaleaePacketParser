# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

from saleae.data import GraphTimeDelta

DISPLAY_FORMAT_CHOICES = {
    'Hex': 'Hex'
}
class Hla(HighLevelAnalyzer):
   
    #temp_frame = None
    # Settings:
    search_for = StringSetting()
    #search_f = StringSetting()
    search_in_type = ChoicesSetting(label='Display Format', choices=DISPLAY_FORMAT_CHOICES.keys())
    #for_spi_test = ChoicesSetting(['MOSI', 'MISO'])
    prefix = StringSetting(label='Message Prefix (optional)')

    result_types = {
        'Sergo': {
            'format': '{{data.decoded}}'
        },
    }
    def __init__(self):

        self.print_cnt = 0

        self.search_index = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.flag_ind =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.match_start_time = None
        self.match_end_time = None
        



        self.search_len = 0
        self.search_raw = []
        nums = self.search_for.split(",")
        base = 10
        for c in nums:
            temp =c.split()
            for i in range(len(temp)):
                temp[i] = int(temp[i],16)
                
            print(temp)
            self.search_raw.append(temp)
               

            self.search_len += 1
        print(len(self.search_raw))


    def decode(self, frame: AnalyzerFrame):

        if (frame.type != 'data' and frame.type != 'result'):
            return
        try:
            if (frame.type == 'data'):
                ch = frame.data['data'][0]
        except:
            return

        #print(frame.data['data'][0])


        for x in range(len(self.search_raw)):
            if ch != self.search_raw[x][self.search_index[x]]:
                self.search_index[x] = 0
            if ch == self.search_raw[x][self.search_index[x]]:
                frames = []
                if self.search_index[x] == 0:
                    self.match_start_time = frame.start_time
                self.search_index[x] = self.search_index[x] + 1

        #if ch != self.search_raw[self.search_index]:
        #    self.search_index = 0
        #    
		#
		#
        #if ch == self.search_raw[self.search_index]:
        #    frames = []
        #    if self.search_index == 0:
        #        self.match_start_time = frame.start_time
        #    self.search_index = self.search_index + 1
        #    if self.search_index == self.search_len:
        #        self.match_end_time = frame.end_time
		#
        #        char = ''
        #        for i in range(self.search_len):
		#
		#
        #            if (self.search_in_type == "Hex"):
		#
        #                char += "%02x " % self.search_raw[i]
		#
        #            else:
		#
        #                char += chr(self.search_raw[i])



         #       frames.append(AnalyzerFrame(
		 #
         #           'Sergo', self.match_start_time, self.match_end_time, {
		 #
         #           'decoded': str(self.prefix) + char.strip()
		 #
         #       }))
		 #
         #       self.search_index = 0
		 #
		 #
		 #
         #   return frames
