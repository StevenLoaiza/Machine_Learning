"""
Gradient Descent
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#sample x values
X_val=np.arange(-14,15)

#create class object
class func_n_grad:
    def __init__(self):
        return self
        
    def myfunc(self):
        func_value=self**2
        return func_value
    def mygrad(self):
        grad_value=2*(self)
        return grad_value

#gradient descent
def grad_desc(startParam,learningRate,iteration):
    #int
    param=-startParam
    X=[]
    Y=[]
    for i in range(iteration):
        X.append(param)
        gradient=func_n_grad.mygrad(param)
        Y.append(gradient)
        param=param-learningRate*gradient
    return X,Y
    

init=func_n_grad
Y_val=init.myfunc(X_val)


param,grad_val=grad_desc(-13,0.1,25)
Y_hat=init.myfunc(np.array(param))
#create the figure
fig = plt.figure() 

#figure size
plt.rcParams["figure.figsize"] = (20,10)

# setting a title for the plot 
plt.title('Gradient Descent Plot',fontsize=18) 

#init ax
ax=plt.axes()

# Create empty lines we are going to plot as part of the animation
line, = ax.plot([], [],color='red',linestyle='dashed',label='Gradient') 
# Static line that will appear on the graph
line2, = ax.plot(X_val,Y_val,color='blue',label= 'Concave Function')


# initialization function 
def init(): 
	# creating an empty plot/frame 
	line.set_data([], []) 
	return line, 

# lists to store x and y axis points 
xdata, ydata = [], [] 

# animation function 
def animate(i): 
	# t is our iteration parameter
	t = i 
	
	# x, y values to be plotted
	xdata = [param[t]-3,param[t],param[t]+3]
	ydata = [-3*grad_val[t]+Y_hat[t],Y_hat[t],3*grad_val[t]+Y_hat[t]]
    #set the appended values into the empty line graph we created
	line.set_data(xdata, ydata) 
	return line
	
    
#add legend
plt.legend(fontsize=15)
#gridline
plt.grid()
# Add x and y lables, and set their font size
plt.xlabel("x values", fontsize=20)
plt.ylabel("y values", fontsize=20)
# Set the font size of the number lables on the axes
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
# Use the FuncAnimation from matplotlib	 
anim = FuncAnimation(fig, animate, init_func=init, 
							frames=len(param), blit=False,interval=200) 

#save GIF
anim.save('gradient_animation.gif')