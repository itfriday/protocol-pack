#!/usr/bin/env python
#coding:utf-8
#=================================================================
# @ Author : Erisenxu @ Innovate Center
# @ Desc : 文件模版
# @ FileName : octemplate.py
# @ Date : 2014-03-29
# @ ModifyHistory :
# @ Remark :
#==================================================================

#
# Object-C文件模版-字段模版
#
OC_H_TEMPLATE = '''/*
 * @(#) ${ClassName}.h Created by @itfriday message creator
 */

#import "PPCompositeField.h"${Imports}

@interface ${ClassName} : PPCompositeField
${Selector}${AttrSetGetDef}
@end
''';

OC_M_TEMPLATE = '''/*
 * @(#) ${ClassName}.m Created by @itfriday message creator
 */

#import "${ClassName}.h"
#import "PPFieldInc.h"
#import "${MsgMacro}.h"

@interface ${ClassName} ()${AttrDefine}
@end

@implementation ${ClassName}

/**
 * 初始化函数
 */
- (instancetype) init {
    if (self = [super init]) {${Inits}
    }
    return self;
}

${AttrSetGet}
/**
 * 字段编码
 * @param buff 保存字段编码后的协议信息
 * @param tag 字段的tag
 * @return 成功返回0，失败返回错误码
 */
- (int) encode:(NSMutableData *)buff tag:(UInt16)tag {
    // 编码TAG
    UInt16 ntag = CFSwapInt16BigToHost(tag);
    [buff appendBytes:&ntag length:sizeof(ntag)];
    // 编码Type
    UInt8 type = FIELD_TYPE_TLV;
    [buff appendBytes:&type length:sizeof(type)];

    // 先将长度设置为0
    UInt32 len = 0;
    [buff appendBytes:&len length:sizeof(len)];

    // 记录下当前数组长度
    UInt32 iArrOldLen = (UInt32)[buff length];

    // 编码子字段${FieldEncode}

    // 修正数组长度
    UInt32 iArrAddLen = (UInt32)[buff length] - iArrOldLen;
    iArrAddLen = CFSwapInt32BigToHost(iArrAddLen);
    [buff replaceBytesInRange:NSMakeRange(iArrOldLen - 4, sizeof(iArrOldLen))
                    withBytes:&iArrAddLen length:sizeof(iArrOldLen)];
    return 0;
}

/**
 * 字段格式化为可读形式
 * @param buff 保存格式化的字符串
 * @param fieldName 字段的名字
 * @param suffix 格式化前缀
 */
- (void) format:(NSMutableString *)buff fieldName:(NSString *)fieldName suffix:(NSString *)suffix {
    NSString* sSubPrefix = [NSString stringWithFormat:@"%@    ", suffix];
    [buff appendFormat:@"%@[%@]\\n", suffix, fieldName];${Formats}
}

/**
 * 字段格式化为xml形式
 * @param buff 保存格式化的字符串
 * @param fieldName 字段的名字
 * @param suffix 格式化前缀
 */
- (void) toXml:(NSMutableString *)buff fieldName:(NSString *)fieldName suffix:(NSString *)suffix {
    NSString* sSubPrefix = [NSString stringWithFormat:@"%@    ", suffix];

    [buff appendFormat:@"%@<%@>\\n", suffix, fieldName];${ToXmls}
    [buff appendFormat:@"%@</%@>\\n", suffix, fieldName];
}

/**
 * 通过标签查询子字段
 * @param tag 子字段的标签
 * @return 返回tag对应的子字段，若没有子字段，返回null
 */
- (id<PPField>) getSubField:(UInt16)tag {
    switch (tag) {${GetSubField}
    default:
        return nil;
    }
}

@end
''';
