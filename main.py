import logging
import hashlib
import json



""" define a constant containing functions representing operators (just sha256 for now) """
OPERATORS = {
    # hash to binary, encode to hex-string
    "sha256" : lambda x: hashlib.sha256(x).digest().encode('hex')
}

class Timestamp:
    def __init__(self, op, prefix, postfix):
        self.operator = op
        self.prefix = prefix
        self.postfix = postfix

"""
Can be used to handle new types of function later
"""
def GetFunctionForOperatorName(operator_name):
    operation_function = OPERATORS[operator_name]

    if operation_function is None:
        raise Exception("don't know which operation to use for " + operator_name)

    return operation_function

"""
Convert a hex-string into opposite-endian binary representation
"""
def ConvertEndian(string_value):
    # reverse the byte-array represented by hex string to opposite-endian and encode back to hex string
    return string_value.decode('hex')[::-1].encode('hex')


"""    
This function should walk through the timestamps and verify message against merkleRoot
Hints: use hashlib.sha256 and hash.hexdigest. message is big-endian while merkleRoot is little-endian.
""" 
def VerifyHash(timestamps, message, merkle_root):

    if len(timestamps) < 1:
        raise ValueError("Unclear what behaviour is expected when there are no timestamps")

    logging.debug("big-endian message {}".format(message))

    for timestamp in timestamps:
        # log timestamp
        logging.debug("Walking through Timestamp({},{},{})".format(timestamp.prefix, timestamp.operator, timestamp.postfix))

        # get a lambda for this operation (just sha256 for now) 
        operator_lambda = GetFunctionForOperatorName(timestamp.operator)

        concatenation = timestamp.prefix + message + timestamp.postfix

         # The output of each operation is Operator(Prefix + message + Postfix), which will become the next message
        logging.debug("creating new message. Operator: {} Operand: {}".format(timestamp.operator, concatenation))

        # we should operate on the binary not the string (so decode string to binary)
        message = operator_lambda(concatenation.decode('hex'))

        logging.debug("new message {}".format(message))


    merkle_root_big_endian = ConvertEndian(merkle_root)

    logging.debug("final message {}".format(message))
    logging.debug("merkle root (little endian) {}".format(merkle_root))
    logging.debug("merkle root (big endian) {}".format(merkle_root_big_endian))
    
    # final message should match merkle_root reversed (converted to big-endian)
    return  message == merkle_root_big_endian

""" unpack data into Timestamps array """
def UnpackJSON(raw_json_string): 
    assert isinstance(raw_json_string, list)

    timestamps = []
    for timestamp in raw_json_string:
        operator = timestamp[0]
        prefix_operand = timestamp[1]
        postfix_operand = timestamp[2]

        timestamps.append(Timestamp(operator, prefix_operand, postfix_operand))

    return timestamps

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    msg = "b4759e820cb549c53c755e5905c744f73605f8f6437ae7884252a5f204c8c6e6"
    merkle_root = "f832e7458a6140ef22c6bc1743f09610281f66a1b202e7b4d278b83de55ef58c"    
    with open("./bag/timestamp.json", "rt") as fp:
        dat = json.load(fp)

        timestamps = UnpackJSON(dat)

        if VerifyHash(timestamps, msg, merkle_root):
            print("CORRECT!")
        else:
            print("INCORRECT!")