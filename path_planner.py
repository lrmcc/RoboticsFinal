
#Path Planner
#
#Module that accepts a list of blob values from image processing, then plans and returns a path to be used by the navigation module


from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from analyze_image import blobDetectionResolution

end_iteration = 0

# Returns a Twist object with information about how to move
def plan_path(blobs, drone_pub, landing_pub):
	global end_iteration

	print("Planning")

	# Determine the largest blob in the image
	# tracked_blob = None
	# maxSize = 0
	# for blob in blobs:
	# 	currX = blob.higherBoundingX - blob.lowerBoundingX
	# 	currY = blob.higherBoundingY - blob.lowerBoundingY
	# 	currSize = currX * currY
	# 	if currSize > maxSize:
	# 		maxSize = currSize
	# 		tracked_blob = blob

	tracked_blob = None
	maxX = 0
	for blob in blobs:
		if blob.averageX > maxX:
			maxX = blob.averageX
			tracked_blob = blob

	if tracked_blob == None:
		print "No blob detected"
		toTurn = 0
		toTranslate = 0
		toDescend = 0
	else:
		toTurn = (.5 - tracked_blob.averageY / float(blobDetectionResolution[0])) * 3
		if tracked_blob.maskValue == 2:
			toTranslate = 0
			toDescend = -.2
			end_iteration += 1
		else:
			toTranslate = 10
			toDescend = 0
			end_iteration = 0
		print "tracked_blob: " + str(tracked_blob.averageX) + " " + str(tracked_blob.averageY) + " " + str(tracked_blob.maskValue)
		print "turn: " + str(toTurn) + " - linear: " + str(toTranslate)

	pos_update = Twist()
	pos_update.angular.z = toTurn
	pos_update.linear.x = toTranslate
	pos_update.linear.z = toDescend

	drone_pub.publish(pos_update)

	if end_iteration == 3:
		landing_pub.publish(Empty())

	return pos_update


#if name == 'main':
 #   print("This is a module. Run main.py instead.")
