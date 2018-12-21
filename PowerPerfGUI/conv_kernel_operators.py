class Conv1x1s1Operators:
    """
    kernel operator must be less than 127.
    """
    Convolution_1x1s1_NEON_Float_NCNN = 0
    Convolution_1x1s1_NEON_Float_NCNNSGEMM = 1
    Convolution_1x1s1_NEON_Float_M1 = 2
    Convolution_1x1s1_NEON_Float_M2 = 3
    Convolution_1x1s1_NEON_Float_M3 = 4
    Convolution_1x1s1_NEON_Float_M4 = 5
    Convolution_1x1s1_NEON_Float_M5 = 6
    Convolution_1x1s1_NEON_Float_M6 = 7
    Convolution_1x1s1_NEON_Int16_M1 = 8
    Convolution_1x1s1_NEON_Int16_M2 = 9
    Convolution_1x1s1_NEON_Int16_M3 = 10
    Convolution_1x1s1_NEON_Int16_M4 = 11
    Convolution_1x1s1_NEON_Int16_M5 = 12
    Convolution_1x1s1_NEON_Int16_M6 = 13
    Convolution_1x1s1_NEON_Int16_M7 = 14
    Convolution_1x1s1_NEON_Int8_NCNN = 15
    Convolution_1x1s1_NEON_Int8_M1 = 16
    Convolution_1x1s1_NEON_Int8_M2 = 17
    ConvType = "Conv1x1s1"
    operators_typeNo = 0
    operators_name = [
        "Convolution_1x1s1_NEON_Float_NCNN",
        "Convolution_1x1s1_NEON_Float_NCNNSGEMM",
        "Convolution_1x1s1_NEON_Float_M1",
        "Convolution_1x1s1_NEON_Float_M2",
        "Convolution_1x1s1_NEON_Float_M3",
        "Convolution_1x1s1_NEON_Float_M4",
        "Convolution_1x1s1_NEON_Float_M5",
        "Convolution_1x1s1_NEON_Float_M6",
        "Convolution_1x1s1_NEON_Int16_M1",
        "Convolution_1x1s1_NEON_Int16_M2",
        "Convolution_1x1s1_NEON_Int16_M3",
        "Convolution_1x1s1_NEON_Int16_M4",
        "Convolution_1x1s1_NEON_Int16_M5",
        "Convolution_1x1s1_NEON_Int16_M6",
        "Convolution_1x1s1_NEON_Int16_M7",
        "Convolution_1x1s1_NEON_Int8_NCNN",
        "Convolution_1x1s1_NEON_Int8_M1",
        "Convolution_1x1s1_NEON_Int8_M2"
    ]


class Conv3x3s1Operators:
    Convolution_3x3s1_NEON_Float_NCNNDirect = 0
    Convolution_3x3s1_NEON_Float_NCNNWinograd = 1
    Convolution_3x3s1_NEON_Float_M1 = 2
    Convolution_3x3s1_NEON_Float_M1_Split = 3
    Convolution_3x3s1_NEON_Float_M2 = 4
    Convolution_3x3s1_NEON_Float_M3 = 5
    Convolution_3x3s1_NEON_Float_M4 = 6
    Convolution_3x3s1_NEON_Float_M5 = 7
    Convolution_3x3s1_NEON_Float_M6 = 8
    Convolution_3x3s1_NEON_Int16_M2 = 9
    Convolution_3x3s1_NEON_Int16_M3 = 10
    Convolution_3x3s1_NEON_Int16_M4 = 11
    Convolution_3x3s1_NEON_Int16_M5 = 12
    Convolution_3x3s1_NEON_Int16_M6 = 13
    Convolution_3x3s1_NEON_Int16_M7 = 14
    Convolution_3x3s1_NEON_Int16_M8 = 15
    Convolution_3x3s1_NEON_Int16_M9 = 16
    Convolution_3x3s1_NEON_Int16_M10 = 17
    Convolution_3x3s1_NEON_Int16_M11 = 18
    Convolution_3x3s1_NEON_Int16_M12 = 19
    Convolution_3x3s1_NEON_Int16_M12_Grouped = 20
    ConvType = "Conv3x3s1"
    operators_typeNo = 1
    operators_name = [
        "Convolution_3x3s1_NEON_Float_NCNNDirect",
        "Convolution_3x3s1_NEON_Float_NCNNWinograd",
        "Convolution_3x3s1_NEON_Float_M1",
        "Convolution_3x3s1_NEON_Float_M1_Split",
        "Convolution_3x3s1_NEON_Float_M2",
        "Convolution_3x3s1_NEON_Float_M3",
        "Convolution_3x3s1_NEON_Float_M4",
        "Convolution_3x3s1_NEON_Float_M5",
        "Convolution_3x3s1_NEON_Float_M6",
        "Convolution_3x3s1_NEON_Int16_M2",
        "Convolution_3x3s1_NEON_Int16_M3",
        "Convolution_3x3s1_NEON_Int16_M4",
        "Convolution_3x3s1_NEON_Int16_M5",
        "Convolution_3x3s1_NEON_Int16_M6",
        "Convolution_3x3s1_NEON_Int16_M7"
        "Convolution_3x3s1_NEON_Int16_M8",
        "Convolution_3x3s1_NEON_Int16_M9",
        "Convolution_3x3s1_NEON_Int16_M10",
        "Convolution_3x3s1_NEON_Int16_M11",
        "Convolution_3x3s1_NEON_Int16_M12",
        "Convolution_3x3s1_NEON_Int16_M12_Grouped"
    ]


class Conv3x3s2Operators:
    Convolution_3x3s2_NEON_Float_NCNN = 0
    Convolution_3x3s2_NEON_Int16_M1 = 1
    ConvType = "Conv3x3s2"
    operators_typeNo = 2
    operators_name = [
        "Convolution_3x3s2_NEON_Float_NCNN",
        "Convolution_3x3s2_NEON_Int16_M1"
    ]


class ConvOperators:
    OperatorTypeKeyWord = ["1x1s1", "3x3s1", "3x3s2"]
    Operators           = [Conv1x1s1Operators(), Conv3x3s1Operators(), Conv3x3s2Operators()]
    OperatorName        = "support all type(CV,NLP,ASR...)"



if __name__ == '__main__':
    # conv_opetaors = ConvOperators()
    # print conv_opetaors.operators_typeNo
    # if "1x1" in  conv_opetaors.Operators[0].operators_name:
    #     print(1111)

    print len(ConvOperators.Operators[0].operators_name)
    print(ConvOperators.Operators[0].operators_typeNo)