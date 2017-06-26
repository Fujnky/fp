import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const


L = 0
J = S = 0.5
gS = -const.value('electron g factor')
gJ = ((gS+1) * J*(J+1) + (gS-1) * (S*(S+1) - L*(L+1))) / (2*J*(J+1))
